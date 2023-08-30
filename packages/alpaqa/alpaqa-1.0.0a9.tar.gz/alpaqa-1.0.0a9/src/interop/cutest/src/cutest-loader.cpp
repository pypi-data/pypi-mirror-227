#include <alpaqa/cutest/cutest-loader.hpp>
#include <alpaqa/util/sparse-ops.hpp>

#include <cutest.h>
#include <dlfcn.h>

#include <cassert>
#include <functional>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>
#include <string_view>
#include <vector>

/*
CUTEST_cfn      : function and constraints values
CUTEST_cofg     : function value and possibly gradient
CUTEST_cofsg    : function value and possibly gradient in sparse format
CUTEST_ccfg     : constraint functions values and possibly gradients
CUTEST_clfg     : Lagrangian function value and possibly gradient
CUTEST_cgr      : constraints gradients and gradient of objective/Lagrangian function
CUTEST_csgr     : constraints gradients and gradient of objective/Lagrangian function
CUTEST_ccfsg    : constraint functions values and possibly their gradients in sparse format
CUTEST_ccifg    : single constraint function value and possibly its gradient
CUTEST_ccifsg   : single constraint function value and possibly gradient in sparse format
CUTEST_cgrdh    : constraints gradients, Hessian of Lagrangian function and gradient of objective/Lagrangian function
CUTEST_cdh      : Hessian of the Lagrangian
CUTEST_cdhc     : Hessian of the constraint part of the Lagrangian
CUTEST_cshp     : sparsity pattern of the Hessian of the Lagrangian function
CUTEST_csh      : Hessian of the Lagrangian, in sparse format
CUTEST_cshc     : Hessian of the constraint part of the Lagrangian, in sparse format
CUTEST_ceh      : sparse Lagrangian Hessian matrix in finite element format
CUTEST_cifn     : problem function value
CUTEST_cigr     : gradient of a problem function
CUTEST_cisgr    : gradient of a problem function in sparse format
CUTEST_cidh     : Hessian of a problem function
CUTEST_cish     : Hessian of an individual problem function, in sparse format
CUTEST_csgrsh   : constraints gradients, sparse Lagrangian Hessian and the gradient of either the objective/Lagrangian in sparse format
CUTEST_csgreh   : constraint gradients, the Lagrangian Hessian in finite element format and the gradient of either the objective/Lagrangian in sparse format
CUTEST_chprod   : matrix-vector product of a vector with the Hessian matrix of the Lagrangian
CUTEST_cshprod  : matrix-vector product of a sparse vector with the Hessian matrix of the Lagrangian
CUTEST_chcprod  : matrix-vector product of a vector with the Hessian matrix of the constraint part of the Lagrangian
CUTEST_cshcprod : matrix-vector product of a spaarse vector with the Hessian matrix of the constraint part of the Lagrangian
CUTEST_cjprod   : matrix-vector product of a vector with the Jacobian of the constraints, or its transpose
CUTEST_csjprod  : matrix-vector product of a sparse vector with the Jacobian of the constraints, or its transpose
CUTEST_cchprods : matrix-vector products of a vector with each of the Hessian matrices of the constraint functions
*/

#ifndef CUTEST_csjp
#define CUTEST_csjp FUNDERSCORE(cutest_csjp)
void CUTEST_csjp(integer *status, integer *nnzj, const integer *lj,
                 integer *J_var, integer *J_con);
#endif

#define STR(x) #x
#define LOAD_DL_FUNC(f) dlfun<decltype(f)>(STR(f))

using namespace std::string_literals;

namespace {
void throw_error(std::string s, int code) {
    throw std::runtime_error(s + " (" + std::to_string(code) + ")");
}
void throw_if_error(std::string s, int code) {
    if (code)
        throw_error(s, code);
}
void log_if_error(std::string s, int code) {
    if (code)
        std::cerr << s << " (" << code << ")\n";
}

std::shared_ptr<void> load_lib(const char *so_filename) {
    assert(so_filename);
    ::dlerror();
    void *h = ::dlopen(so_filename, RTLD_LOCAL | RTLD_NOW);
    if (auto *err = ::dlerror())
        throw std::runtime_error(err);
    return std::shared_ptr<void>{h, &::dlclose};
}
} // namespace

namespace alpaqa {

class CUTEstLoader {
  public:
    USING_ALPAQA_CONFIG(CUTEstProblem::config_t);
    using Box = alpaqa::Box<config_t>;

  private:
    using cleanup_t = std::shared_ptr<void>;
    template <class F>
    cleanup_t cleanup(F &&func) {
        return cleanup_t{nullptr,
                         [func{std::forward<F>(func)}](void *) { func(); }};
    }

    cleanup_t load_outsdif(const char *outsdif_fname) {
        integer status;
        auto fptr_open  = LOAD_DL_FUNC(FORTRAN_open);
        auto fptr_close = LOAD_DL_FUNC(FORTRAN_close);
        fptr_open(&funit, outsdif_fname, &status);
        throw_if_error("Failed to open "s + outsdif_fname, status);
        return cleanup([funit{this->funit}, fptr_close] {
            integer status;
            fptr_close(&funit, &status);
            log_if_error("Failed to close OUTSDIF.d file", status);
        });
    }

    cleanup_t terminator() {
        auto fptr_cterminate = LOAD_DL_FUNC(CUTEST_cterminate);
        return cleanup([fptr_cterminate] {
            integer status;
            fptr_cterminate(&status);
            log_if_error("Failed to call cutest_cterminate", status);
        });
    }

  public:
    CUTEstLoader(const char *so_fname, const char *outsdif_fname) {
        // Open the shared library
        so_handle = load_lib(so_fname);

        // Open the OUTSDIF.d file
        cleanup_outsdif = load_outsdif(outsdif_fname);

        // Get the dimensions of the problem
        integer status;
        auto fptr_cdimen = LOAD_DL_FUNC(CUTEST_cdimen);
        fptr_cdimen(&status, &funit, &nvar, &ncon);
        throw_if_error("Failed to call cutest_cdimen", status);
    }

    struct ConstrFuncs {
        decltype(CUTEST_cfn) *cfn;
        decltype(CUTEST_cofg) *cofg;
        decltype(CUTEST_ccfg) *ccfg;
        decltype(CUTEST_clfg) *clfg;
        decltype(CUTEST_cjprod) *cjprod;
        decltype(CUTEST_ccifg) *ccifg;
        decltype(CUTEST_cigr) *cigr;
        decltype(CUTEST_cdimsj) *cdimsj;
        decltype(CUTEST_csjp) *csjp;
        decltype(CUTEST_ccfsg) *ccfsg;
        decltype(CUTEST_cdh) *cdh;
        decltype(CUTEST_cdimsh) *cdimsh;
        decltype(CUTEST_cshp) *cshp;
        decltype(CUTEST_csh) *csh;
        decltype(CUTEST_chprod) *chprod;
    };

    void setup_problem(rvec x0, rvec y0, Box &C, Box &D) {
        assert(x0.size() == static_cast<length_t>(nvar));
        assert(C.lowerbound.size() == static_cast<length_t>(nvar));
        assert(C.upperbound.size() == static_cast<length_t>(nvar));
        assert(y0.size() == static_cast<length_t>(ncon));
        assert(D.lowerbound.size() == static_cast<length_t>(ncon));
        assert(D.upperbound.size() == static_cast<length_t>(ncon));
        equatn.resize(static_cast<length_t>(ncon));
        linear.resize(static_cast<length_t>(ncon));
        integer e_order = 0; // no specific order of equality constraints
        integer l_order = 0; // no specific order of linear constraints
        integer v_order = 0; // no specific order of linear variables
        integer status;

        LOAD_DL_FUNC(CUTEST_csetup)
        (&status, &funit, &iout, &io_buffer, &nvar, &ncon, x0.data(),
         C.lowerbound.data(), C.upperbound.data(), y0.data(),
         D.lowerbound.data(), D.upperbound.data(), equatn.data(), linear.data(),
         &e_order, &l_order, &v_order);
        throw_if_error("Failed to call cutest_csetup", status);
        cutest_terminate = terminator();
        if (ncon == 0)
            throw std::runtime_error(
                "Unconstrained CUTEst problems are currently unsupported");
        work.resize(std::max(nvar, ncon));
        work2.resize(std::max(nvar, ncon));
        std::replace(C.lowerbound.begin(), C.lowerbound.end(), -CUTE_INF,
                     -inf<config_t>);
        std::replace(C.upperbound.begin(), C.upperbound.end(), +CUTE_INF,
                     +inf<config_t>);
        std::replace(D.lowerbound.begin(), D.lowerbound.end(), -CUTE_INF,
                     -inf<config_t>);
        std::replace(D.upperbound.begin(), D.upperbound.end(), +CUTE_INF,
                     +inf<config_t>);
        funcs = {
            .cfn    = LOAD_DL_FUNC(CUTEST_cfn),
            .cofg   = LOAD_DL_FUNC(CUTEST_cofg),
            .ccfg   = LOAD_DL_FUNC(CUTEST_ccfg),
            .clfg   = LOAD_DL_FUNC(CUTEST_clfg),
            .cjprod = LOAD_DL_FUNC(CUTEST_cjprod),
            .ccifg  = LOAD_DL_FUNC(CUTEST_ccifg),
            .cigr   = LOAD_DL_FUNC(CUTEST_cigr),
            .cdimsj = LOAD_DL_FUNC(CUTEST_cdimsj),
            .csjp   = LOAD_DL_FUNC(CUTEST_csjp),
            .ccfsg  = LOAD_DL_FUNC(CUTEST_ccfsg),
            .cdh    = LOAD_DL_FUNC(CUTEST_cdh),
            .cdimsh = LOAD_DL_FUNC(CUTEST_cdimsh),
            .cshp   = LOAD_DL_FUNC(CUTEST_cshp),
            .csh    = LOAD_DL_FUNC(CUTEST_csh),
            .chprod = LOAD_DL_FUNC(CUTEST_chprod),
        };
    }

    std::string get_name() {
        std::string name(FSTRING_LEN, ' ');
        integer status;
        LOAD_DL_FUNC(CUTEST_probname)(&status, name.data());
        throw_if_error("Failed to call CUTEST_probname", status);
        if (auto last = name.find_last_not_of(' '); last != name.npos)
            name.resize(last + 1);
        return name;
    }

    integer get_report(doublereal *calls, doublereal *time) {
        integer status;
        auto fptr_report = ncon > 0 ? LOAD_DL_FUNC(CUTEST_creport)
                                    : LOAD_DL_FUNC(CUTEST_ureport);
        fptr_report(&status, calls, time);
        return status;
    }

    template <class T>
    T *dlfun(const char *name) {
        (void)dlerror();
        auto res = reinterpret_cast<T *>(::dlsym(so_handle.get(), name));
        if (const char *error = dlerror())
            throw std::runtime_error(error);
        return res;
    }

    // Order of cleanup is important!
    std::shared_ptr<void> so_handle; ///< dlopen handle to shared library
    cleanup_t cleanup_outsdif;  ///< Responsible for closing the OUTSDIF.d file
    cleanup_t cutest_terminate; ///< Responsible for calling CUTEST_xterminate

    integer funit     = 42; ///< Fortran Unit Number for OUTSDIF.d file
    integer iout      = 6;  ///< Fortran Unit Number for standard output
    integer io_buffer = 11; ///< Fortran Unit Number for internal IO

    integer nvar;      ///< Number of decision variabls
    integer ncon;      ///< Number of constraints
    ConstrFuncs funcs; /// Pointers to loaded problem functions

    using logical_vec = Eigen::VectorX<logical>;
    logical_vec equatn;      ///< whether the constraint is an equality
    logical_vec linear;      ///< whether the constraint is linear
    mutable vec work, work2; ///< work vectors
};

CUTEstProblem::CUTEstProblem(const char *so_fname, const char *outsdif_fname,
                             bool sparse)
    : BoxConstrProblem<config_t>{0, 0}, sparse{sparse} {
    impl = std::make_unique<CUTEstLoader>(so_fname, outsdif_fname);
    resize(static_cast<length_t>(impl->nvar),
           static_cast<length_t>(impl->ncon));
    x0.resize(n);
    y0.resize(m);
    impl->setup_problem(x0, y0, C, D);
    name = impl->get_name();
}

CUTEstProblem::CUTEstProblem(const CUTEstProblem &)                = default;
CUTEstProblem &CUTEstProblem::operator=(const CUTEstProblem &)     = default;
CUTEstProblem::CUTEstProblem(CUTEstProblem &&) noexcept            = default;
CUTEstProblem &CUTEstProblem::operator=(CUTEstProblem &&) noexcept = default;
CUTEstProblem::~CUTEstProblem()                                    = default;

CUTEstProblem::Report CUTEstProblem::get_report() const {
    double calls[7];
    double time[2];
    Report r;
    using stat_t           = decltype(r.status);
    r.status               = static_cast<stat_t>(impl->get_report(calls, time));
    r.name                 = impl->get_name();
    r.nvar                 = impl->nvar;
    r.ncon                 = impl->ncon;
    r.calls.objective      = static_cast<unsigned>(calls[0]);
    r.calls.objective_grad = static_cast<unsigned>(calls[1]);
    r.calls.objective_hess = static_cast<unsigned>(calls[2]);
    r.calls.hessian_times_vector = static_cast<unsigned>(calls[3]);
    r.calls.constraints = impl->ncon > 0 ? static_cast<unsigned>(calls[4]) : 0;
    r.calls.constraints_grad =
        impl->ncon > 0 ? static_cast<unsigned>(calls[5]) : 0;
    r.calls.constraints_hess =
        impl->ncon > 0 ? static_cast<unsigned>(calls[6]) : 0;
    r.time_setup = time[0];
    r.time       = time[1];
    return r;
}

auto CUTEstProblem::eval_f(crvec x) const -> real_t {
    assert(x.size() == static_cast<length_t>(impl->nvar));
    integer status;
    real_t f;
    logical grad = FALSE_;
    impl->funcs.cofg(&status, &impl->nvar, x.data(), &f, nullptr, &grad);
    throw_if_error("eval_f: CUTEST_cofg", status);
    return f;
}
void CUTEstProblem::eval_grad_f(crvec x, rvec grad_fx) const {
    assert(x.size() == static_cast<length_t>(impl->nvar));
    assert(grad_fx.size() == static_cast<length_t>(impl->nvar));
    integer status;
    real_t f;
    logical grad = TRUE_;
    impl->funcs.cofg(&status, &impl->nvar, x.data(), &f, grad_fx.data(), &grad);
    throw_if_error("eval_grad_f: CUTEST_cofg", status);
}
void CUTEstProblem::eval_g(crvec x, rvec gx) const {
    assert(x.size() == static_cast<length_t>(impl->nvar));
    assert(gx.size() == static_cast<length_t>(impl->ncon));
    integer status;
    logical jtrans = TRUE_, grad = FALSE_;
    integer zero = 0;
    impl->funcs.ccfg(&status, &impl->nvar, &impl->ncon, x.data(), gx.data(),
                     &jtrans, &zero, &zero, nullptr, &grad);
    throw_if_error("eval_g: CUTEST_ccfg", status);
}
void CUTEstProblem::eval_grad_g_prod(crvec x, crvec y, rvec grad_gxy) const {
    assert(x.size() == static_cast<length_t>(impl->nvar));
    assert(y.size() == static_cast<length_t>(impl->ncon));
    assert(grad_gxy.size() == static_cast<length_t>(impl->nvar));
    integer status;
    auto lvector = static_cast<integer>(y.size()),
         lresult = static_cast<integer>(grad_gxy.size());
    logical gotj = FALSE_, jtrans = TRUE_;
    impl->funcs.cjprod(&status, &impl->nvar, &impl->ncon, &gotj, &jtrans,
                       x.data(), y.data(), &lvector, grad_gxy.data(), &lresult);
    throw_if_error("eval_grad_g_prod: CUTEST_cjprod", status);
}

void CUTEstProblem::eval_jac_g(crvec x, [[maybe_unused]] rindexvec inner_idx,
                               [[maybe_unused]] rindexvec outer_ptr,
                               rvec J_values) const {
    // Compute the nonzero values
    if (J_values.size() > 0) {
        assert(x.size() == static_cast<length_t>(impl->nvar));
        integer status;
        // Sparse Jacobian
        if (sparse) {
            assert(nnz_J >= 0);
            assert(J_values.size() == static_cast<length_t>(nnz_J));
            assert(J_work.size() == static_cast<length_t>(nnz_J));
            assert(inner_idx.size() == static_cast<length_t>(nnz_J));
            assert(outer_ptr.size() == static_cast<length_t>(impl->nvar + 1));
            const integer nnz = nnz_J;
            logical grad      = TRUE_;
            impl->funcs.ccfsg(&status, &impl->nvar, &impl->ncon, x.data(),
                              impl->work.data(), &nnz_J, &nnz, J_work.data(),
                              J_col.data(), J_row.data(), &grad);
            throw_if_error("eval_jac_g: CUTEST_ccfsg", status);
            auto t0  = std::chrono::steady_clock::now();
            J_values = J_work(J_perm);
            auto t1  = std::chrono::steady_clock::now();
            std::cout << "Permutation of J took: "
                      << std::chrono::duration<double>{t1 - t0}.count() * 1e6
                      << " µs\n";
        }
        // Dense Jacobian
        else {
            assert(J_values.size() == static_cast<length_t>(impl->nvar) *
                                          static_cast<length_t>(impl->ncon));
            integer status;
            logical jtrans = FALSE_, grad = TRUE_;
            impl->funcs.ccfg(&status, &impl->nvar, &impl->ncon, x.data(),
                             impl->work.data(), &jtrans, &impl->ncon,
                             &impl->nvar, J_values.data(), &grad);
            throw_if_error("eval_jac_g: CUTEST_ccfg", status);
        }
    }
    // Compute sparsity pattern without values
    else {
        assert(nnz_J >= 0);
        assert(inner_idx.size() == static_cast<length_t>(nnz_J));
        assert(outer_ptr.size() == static_cast<length_t>(impl->nvar + 1));
        integer status;
        const integer nnz = nnz_J;
        impl->funcs.csjp(&status, &nnz_J, &nnz, J_col.data(), J_row.data());
        throw_if_error("eval_jac_g: CUTEST_csjp", status);
        std::iota(J_perm.begin(), J_perm.end(), index_t{0});
        util::sort_triplets(J_row, J_col, J_perm);
        util::convert_triplets_to_ccs<config_t>(J_row, J_col, inner_idx,
                                                outer_ptr, 1);
    }
}
auto CUTEstProblem::get_jac_g_num_nonzeros() const -> length_t {
    if (!sparse)
        return -1;
    if (nnz_J < 0) {
        integer status;
        impl->funcs.cdimsj(&status, &nnz_J);
        throw_if_error("get_jac_g_num_nonzeros: CUTEST_cdimsj", status);
        nnz_J -= impl->nvar;
        assert(nnz_J >= 0);
        J_col.resize(nnz_J);
        J_row.resize(nnz_J);
        J_perm.resize(nnz_J);
        J_work.resize(nnz_J);
    }
    return nnz_J;
}
void CUTEstProblem::eval_grad_gi(crvec x, index_t i, rvec grad_gi) const {
    assert(x.size() == static_cast<length_t>(impl->nvar));
    assert(grad_gi.size() == static_cast<length_t>(impl->nvar));
    integer status;
    auto iprob = static_cast<integer>(i + 1);
    impl->funcs.cigr(&status, &impl->nvar, &iprob, x.data(), grad_gi.data());
    throw_if_error("eval_grad_gi: CUTEST_cigr", status);
}
void CUTEstProblem::eval_hess_L_prod(crvec x, crvec y, real_t scale, crvec v,
                                     rvec Hv) const {
    assert(x.size() == static_cast<length_t>(impl->nvar));
    assert(y.size() == static_cast<length_t>(impl->ncon));
    assert(v.size() == static_cast<length_t>(impl->nvar));
    assert(Hv.size() == static_cast<length_t>(impl->nvar));
    const auto *mult = y.data();
    if (scale != 1) {
        impl->work = y * (real_t(1) / scale);
        mult       = impl->work.data();
    }
    integer status;
    logical goth = FALSE_;
    impl->funcs.chprod(&status, &impl->nvar, &impl->ncon, &goth, x.data(), mult,
                       const_cast<real_t *>(v.data()), Hv.data());
    throw_if_error("eval_hess_L_prod: CUTEST_chprod", status);
    if (scale != 1)
        Hv *= scale;
}
void CUTEstProblem::eval_hess_ψ_prod(crvec x, crvec y, crvec Σ, real_t scale,
                                     crvec v, rvec Hv) const {
    assert(x.size() == static_cast<length_t>(impl->nvar));
    assert(y.size() == static_cast<length_t>(impl->ncon));
    assert(Σ.size() == static_cast<length_t>(impl->ncon));
    assert(v.size() == static_cast<length_t>(impl->nvar));
    assert(Hv.size() == static_cast<length_t>(impl->nvar));
    auto &&ζ = impl->work.topRows(impl->ncon);
    auto &&ŷ = impl->work2.topRows(impl->ncon);
    // ζ = g(x) + Σ⁻¹y
    eval_g(x, ζ);
    ζ += Σ.asDiagonal().inverse() * y;
    // d = ζ - Π(ζ, D)
    this->eval_proj_diff_g(ζ, ŷ);
    // ŷ = Σ d
    ŷ.array() *= Σ.array();
    // Hv = ∇²ℒ(x, ŷ) v
    eval_hess_L_prod(x, ŷ, scale, v, Hv);
    // Find active constraints
    for (index_t i = 0; i < impl->ncon; ++i)
        ζ(i) = (ζ(i) <= D.lowerbound(i)) || (D.upperbound(i) <= ζ(i))
                   ? Σ(i)
                   : real_t(0);
    // Jg(x) v
    auto &&Jv = impl->work2.topRows(impl->ncon);
    integer status;
    auto lvector = static_cast<integer>(v.size()),
         lresult = static_cast<integer>(Jv.size());
    logical gotj = FALSE_, jtrans = FALSE_;
    impl->funcs.cjprod(&status, &impl->nvar, &impl->ncon, &gotj, &jtrans,
                       x.data(), v.data(), &lvector, Jv.data(), &lresult);
    throw_if_error("eval_hess_ψ_prod: CUTEST_cjprod-1", status);
    // Σ Jg v
    Jv.array() *= ζ.array();
    // Jgᵀ Σ Jg v
    std::swap(lvector, lresult);
    gotj = jtrans = TRUE_;
    auto &&JΣJv   = impl->work.topRows(impl->nvar);
    impl->funcs.cjprod(&status, &impl->nvar, &impl->ncon, &gotj, &jtrans,
                       x.data(), Jv.data(), &lvector, JΣJv.data(), &lresult);
    throw_if_error("eval_hess_ψ_prod: CUTEST_cjprod-2", status);
    Hv += JΣJv;
}
void CUTEstProblem::eval_hess_L(crvec x, crvec y, real_t scale,
                                rindexvec inner_idx, rindexvec outer_ptr,
                                rvec H_values) const {
    // Compute the nonzero values
    if (H_values.size() > 0) {
        assert(x.size() == static_cast<length_t>(impl->nvar));
        assert(y.size() == static_cast<length_t>(impl->ncon));
        const auto *mult = y.data();
        if (scale != 1) {
            impl->work = y * (real_t(1) / scale);
            mult       = impl->work.data();
        }
        integer status;
        // Sparse Hessian
        if (sparse) {
            assert(nnz_H >= 0);
            assert(H_values.size() == static_cast<length_t>(nnz_H));
            assert(H_work.size() == static_cast<length_t>(nnz_H));
            assert(inner_idx.size() == static_cast<length_t>(nnz_H));
            assert(outer_ptr.size() == static_cast<length_t>(impl->nvar + 1));
            const integer nnz = nnz_H;
            impl->funcs.csh(&status, &impl->nvar, &impl->ncon, x.data(),
                            y.data(), &nnz_H, &nnz, H_work.data(), H_col.data(),
                            H_row.data());
            throw_if_error("eval_hess_L: CUTEST_csh", status);
            auto t0  = std::chrono::steady_clock::now();
            H_values = H_work(H_perm);
            auto t1  = std::chrono::steady_clock::now();
            std::cout << "Permutation of H took: "
                      << std::chrono::duration<double>{t1 - t0}.count() * 1e6
                      << " µs\n";
        }
        // Dense Hessian
        else {
            assert(H_values.size() == static_cast<length_t>(impl->nvar) *
                                          static_cast<length_t>(impl->nvar));
            impl->funcs.cdh(&status, &impl->nvar, &impl->ncon, x.data(), mult,
                            &impl->nvar, H_values.data());
            throw_if_error("eval_hess_L: CUTEST_cdh", status);
        }
        if (scale != 1)
            H_values *= scale;
    }
    // Compute sparsity pattern without values
    else {
        assert(nnz_H >= 0);
        assert(inner_idx.size() == static_cast<length_t>(nnz_H));
        assert(outer_ptr.size() == static_cast<length_t>(impl->nvar + 1));
        integer status;
        const integer nnz = nnz_H;
        impl->funcs.cshp(&status, &impl->nvar, &nnz_H, &nnz, H_row.data(),
                         H_col.data());
        throw_if_error("eval_hess_L: CUTEST_cshp", status);
        std::iota(H_perm.begin(), H_perm.end(), index_t{0});
        util::sort_triplets(H_row, H_col, H_perm);
        util::convert_triplets_to_ccs<config_t>(H_row, H_col, inner_idx,
                                                outer_ptr, 1);
    }
}
auto CUTEstProblem::get_hess_L_num_nonzeros() const -> length_t {
    if (!sparse)
        return -1;
    if (nnz_H < 0) {
        integer status;
        impl->funcs.cdimsh(&status, &nnz_H);
        throw_if_error("get_hess_L_num_nonzeros: CUTEST_cdimsh", status);
        assert(nnz_H >= 0);
        H_col.resize(nnz_H);
        H_row.resize(nnz_H);
        H_perm.resize(nnz_H);
        H_work.resize(nnz_H);
    }
    return nnz_H;
}
auto CUTEstProblem::eval_f_grad_f(crvec x, rvec grad_fx) const -> real_t {
    assert(x.size() == static_cast<length_t>(impl->nvar));
    assert(grad_fx.size() == static_cast<length_t>(impl->nvar));
    integer status;
    real_t f;
    logical grad = TRUE_;
    impl->funcs.cofg(&status, &impl->nvar, x.data(), &f, grad_fx.data(), &grad);
    throw_if_error("eval_f_grad_f: CUTEST_cofg", status);
    return f;
}
auto CUTEstProblem::eval_f_g(crvec x, rvec g) const -> real_t {
    assert(x.size() == static_cast<length_t>(impl->nvar));
    assert(g.size() == static_cast<length_t>(impl->ncon));
    integer status;
    real_t f;
    impl->funcs.cfn(&status, &impl->nvar, &impl->ncon, x.data(), &f, g.data());
    throw_if_error("eval_f_g: CUTEST_cfn", status);
    return f;
}
void CUTEstProblem::eval_grad_L(crvec x, crvec y, rvec grad_L, rvec) const {
    assert(x.size() == static_cast<length_t>(impl->nvar));
    assert(y.size() == static_cast<length_t>(impl->ncon));
    assert(grad_L.size() == static_cast<length_t>(impl->nvar));
    integer status;
    real_t L;
    logical grad = TRUE_;
    impl->funcs.clfg(&status, &impl->nvar, &impl->ncon, x.data(), y.data(), &L,
                     grad_L.data(), &grad);
    throw_if_error("eval_f_g: CUTEST_clfg", status);
}

const char *enum_name(CUTEstProblem::Report::Status s) {
    using Status = CUTEstProblem::Report::Status;
    switch (s) {
        case Status::Success: return "Success";
        case Status::AllocationError: return "AllocationError";
        case Status::ArrayBoundError: return "ArrayBoundError";
        case Status::EvaluationError: return "EvaluationError";
        default:;
    }
    throw std::out_of_range(
        "invalid value for pa::CUTEstProblem::Report::Status");
}

std::ostream &operator<<(std::ostream &os, CUTEstProblem::Report::Status s) {
    return os << enum_name(s);
}

std::ostream &operator<<(std::ostream &os, const CUTEstProblem::Report &r) {
    os << "CUTEst problem: " << r.name << "\r\n\n"                 //
       << "Number of variables:   " << r.nvar << "\r\n"            //
       << "Number of constraints: " << r.ncon << "\r\n\n"          //
       << "Status: " << r.status << " (" << +r.status << ")\r\n\n" //
       << "Objective function evaluations:            " << r.calls.objective
       << "\r\n"
       << "Objective function gradient evaluations:   "
       << r.calls.objective_grad << "\r\n"
       << "Objective function Hessian evaluations:    "
       << r.calls.objective_hess << "\r\n"
       << "Hessian times vector products:             "
       << r.calls.objective_hess << "\r\n\n";
    if (r.ncon > 0) {
        os << "Constraint function evaluations:           "
           << r.calls.constraints << "\r\n"
           << "Constraint function gradients evaluations: "
           << r.calls.constraints_grad << "\r\n"
           << "Constraint function Hessian evaluations:   "
           << r.calls.constraints_hess << "\r\n\n";
    }
    return os << "Setup time:       " << r.time_setup << "s\r\n"
              << "Time since setup: " << r.time << "s";
}

} // namespace alpaqa