#include <gtest/gtest.h>

#include <vector>
#include <memory>

#include "tatami/dense/DenseMatrix.hpp"
#include "tatami/isometric/unary/DelayedUnaryIsometricOp.hpp"
#include "tatami/utils/convert_to_sparse.hpp"

#include "tatami_test/tatami_test.hpp"
#include "../utils.h"

class CompareVectorTest : public ::testing::TestWithParam<std::tuple<bool, bool> > {
protected:
    size_t nrow = 291, ncol = 188;
    std::shared_ptr<tatami::NumericMatrix> dense, sparse;
    std::vector<double> simulated;
protected:
    void SetUp() {
        simulated = tatami_test::simulate_sparse_vector<double>(nrow * ncol, 0.1, -3, 3);
        for (auto& x : simulated) {
            if (x) {
                // Rounding for easier tests of exact equality.
                x = std::round(x);
                if (x == 0) {
                    x = 1;
                }
            }
        }

        dense = std::shared_ptr<tatami::NumericMatrix>(new tatami::DenseRowMatrix<double>(nrow, ncol, simulated));
        sparse = tatami::convert_to_sparse<false>(dense.get()); // column major.
        return;
    }

    static void fill_default_vector(std::vector<double>& vec) {
        int val = 1;
        for (auto& x : vec) {
            x = (val % 3) - 1;
            ++val;
        }
    }
};

TEST_P(CompareVectorTest, Equal) {
    auto param = GetParam();
    bool row = std::get<0>(param);
    bool is_sparse = std::get<1>(param);

    std::vector<double> vec(row ? nrow : ncol);
    if (is_sparse) {
        int val = 1;
        for (auto& x : vec) {
            // i.e., no zero equality here.
            x = (val % 2 ? 1 : -1);
            ++val;
        }
    } else {
        fill_default_vector(vec);
    }

    std::shared_ptr<tatami::NumericMatrix> dense_mod, sparse_mod;
    if (row) {
        auto op = tatami::make_DelayedEqualVectorHelper<0>(vec);
        dense_mod = tatami::make_DelayedUnaryIsometricOp(this->dense, op);
        sparse_mod = tatami::make_DelayedUnaryIsometricOp(this->sparse, op);
    } else {
        auto op = tatami::make_DelayedEqualVectorHelper<1>(vec);
        dense_mod = tatami::make_DelayedUnaryIsometricOp(this->dense, op);
        sparse_mod = tatami::make_DelayedUnaryIsometricOp(this->sparse, op);
    }

    EXPECT_FALSE(dense_mod->sparse());
    EXPECT_EQ(dense->nrow(), dense_mod->nrow());
    EXPECT_EQ(dense->ncol(), dense_mod->ncol());
    if (is_sparse) {
        EXPECT_TRUE(sparse_mod->sparse());
    } else {
        EXPECT_FALSE(sparse_mod->sparse());
    }

    auto refvec = this->simulated;
    for (size_t r = 0; r < this->nrow; ++r) {
        for (size_t c = 0; c < this->ncol; ++c) {
            auto& x = refvec[r * this->ncol + c];
            x = (x == vec[row ? r : c]);
        }
    }
    
    tatami::DenseRowMatrix<double> ref(this->nrow, this->ncol, std::move(refvec));
    quick_test_all(dense_mod.get(), &ref);
    quick_test_all(sparse_mod.get(), &ref);
}

TEST_P(CompareVectorTest, GreaterThan) {
    auto param = GetParam();
    bool row = std::get<0>(param);
    bool is_sparse = std::get<1>(param);

    std::vector<double> vec(row ? nrow : ncol);
    if (is_sparse) {
        int val = 1;
        for (auto& x : vec) {
            x = (val % 3);
            ++val;
        }
    } else {
        fill_default_vector(vec);
    }

    std::shared_ptr<tatami::NumericMatrix> dense_mod, sparse_mod;
    if (row) {
        auto op = tatami::make_DelayedGreaterThanVectorHelper<0>(vec);
        dense_mod = tatami::make_DelayedUnaryIsometricOp(this->dense, op);
        sparse_mod = tatami::make_DelayedUnaryIsometricOp(this->sparse, op);
    } else {
        auto op = tatami::make_DelayedGreaterThanVectorHelper<1>(vec);
        dense_mod = tatami::make_DelayedUnaryIsometricOp(this->dense, op);
        sparse_mod = tatami::make_DelayedUnaryIsometricOp(this->sparse, op);
    }

    EXPECT_FALSE(dense_mod->sparse());
    EXPECT_EQ(dense->nrow(), dense_mod->nrow());
    EXPECT_EQ(dense->ncol(), dense_mod->ncol());
    if (is_sparse) {
        EXPECT_TRUE(sparse_mod->sparse());
    } else {
        EXPECT_FALSE(sparse_mod->sparse());
    }

    auto refvec = this->simulated;
    for (size_t r = 0; r < this->nrow; ++r) {
        for (size_t c = 0; c < this->ncol; ++c) {
            auto& x = refvec[r * this->ncol + c];
            x = (x > vec[row ? r : c]);
        }
    }
    
    tatami::DenseRowMatrix<double> ref(this->nrow, this->ncol, std::move(refvec));
    quick_test_all(dense_mod.get(), &ref);
    quick_test_all(sparse_mod.get(), &ref);
}

TEST_P(CompareVectorTest, LessThan) {
    auto param = GetParam();
    bool row = std::get<0>(param);
    bool is_sparse = std::get<1>(param);

    std::vector<double> vec(row ? nrow : ncol);
    if (is_sparse) {
        int val = 1;
        for (auto& x : vec) {
            x = -(val % 3);
            ++val;
        }
    } else {
        fill_default_vector(vec);
    }

    std::shared_ptr<tatami::NumericMatrix> dense_mod, sparse_mod;
    if (row) {
        auto op = tatami::make_DelayedLessThanVectorHelper<0>(vec);
        dense_mod = tatami::make_DelayedUnaryIsometricOp(this->dense, op);
        sparse_mod = tatami::make_DelayedUnaryIsometricOp(this->sparse, op);
    } else {
        auto op = tatami::make_DelayedLessThanVectorHelper<1>(vec);
        dense_mod = tatami::make_DelayedUnaryIsometricOp(this->dense, op);
        sparse_mod = tatami::make_DelayedUnaryIsometricOp(this->sparse, op);
    }

    EXPECT_FALSE(dense_mod->sparse());
    EXPECT_EQ(dense->nrow(), dense_mod->nrow());
    EXPECT_EQ(dense->ncol(), dense_mod->ncol());
    if (is_sparse) {
        EXPECT_TRUE(sparse_mod->sparse());
    } else {
        EXPECT_FALSE(sparse_mod->sparse());
    }

    auto refvec = this->simulated;
    for (size_t r = 0; r < this->nrow; ++r) {
        for (size_t c = 0; c < this->ncol; ++c) {
            auto& x = refvec[r * this->ncol + c];
            x = (x < vec[row ? r : c]);
        }
    }
    
    tatami::DenseRowMatrix<double> ref(this->nrow, this->ncol, std::move(refvec));
    quick_test_all(dense_mod.get(), &ref);
    quick_test_all(sparse_mod.get(), &ref);
}

TEST_P(CompareVectorTest, GreaterThanOrEqual) {
    auto param = GetParam();
    bool row = std::get<0>(param);
    bool is_sparse = std::get<1>(param);

    std::vector<double> vec(row ? nrow : ncol);
    if (is_sparse) {
        int val = 1;
        for (auto& x : vec) {
            x = (val % 2 ? 1.0 : 1.5);
            ++val;
        }
    } else {
        fill_default_vector(vec);
    }

    std::shared_ptr<tatami::NumericMatrix> dense_mod, sparse_mod;
    if (row) {
        auto op = tatami::make_DelayedGreaterThanOrEqualVectorHelper<0>(vec);
        dense_mod = tatami::make_DelayedUnaryIsometricOp(this->dense, op);
        sparse_mod = tatami::make_DelayedUnaryIsometricOp(this->sparse, op);
    } else {
        auto op = tatami::make_DelayedGreaterThanOrEqualVectorHelper<1>(vec);
        dense_mod = tatami::make_DelayedUnaryIsometricOp(this->dense, op);
        sparse_mod = tatami::make_DelayedUnaryIsometricOp(this->sparse, op);
    }

    EXPECT_FALSE(dense_mod->sparse());
    EXPECT_EQ(dense->nrow(), dense_mod->nrow());
    EXPECT_EQ(dense->ncol(), dense_mod->ncol());
    if (is_sparse) {
        EXPECT_TRUE(sparse_mod->sparse());
    } else {
        EXPECT_FALSE(sparse_mod->sparse());
    }

    auto refvec = this->simulated;
    for (size_t r = 0; r < this->nrow; ++r) {
        for (size_t c = 0; c < this->ncol; ++c) {
            auto& x = refvec[r * this->ncol + c];
            x = (x >= vec[row ? r : c]);
        }
    }
    
    tatami::DenseRowMatrix<double> ref(this->nrow, this->ncol, std::move(refvec));
    quick_test_all(dense_mod.get(), &ref);
    quick_test_all(sparse_mod.get(), &ref);
}

TEST_P(CompareVectorTest, LessThanOrEqual) {
    auto param = GetParam();
    bool row = std::get<0>(param);
    bool is_sparse = std::get<1>(param);

    std::vector<double> vec(row ? nrow : ncol);
    if (is_sparse) {
        int val = 1;
        for (auto& x : vec) {
            x = (val % 2 ? -1.0 : -2.0);
            ++val;
        }
    } else {
        fill_default_vector(vec);
    }

    std::shared_ptr<tatami::NumericMatrix> dense_mod, sparse_mod;
    if (row) {
        auto op = tatami::make_DelayedLessThanOrEqualVectorHelper<0>(vec);
        dense_mod = tatami::make_DelayedUnaryIsometricOp(this->dense, op);
        sparse_mod = tatami::make_DelayedUnaryIsometricOp(this->sparse, op);
    } else {
        auto op = tatami::make_DelayedLessThanOrEqualVectorHelper<1>(vec);
        dense_mod = tatami::make_DelayedUnaryIsometricOp(this->dense, op);
        sparse_mod = tatami::make_DelayedUnaryIsometricOp(this->sparse, op);
    }

    EXPECT_FALSE(dense_mod->sparse());
    EXPECT_EQ(dense->nrow(), dense_mod->nrow());
    EXPECT_EQ(dense->ncol(), dense_mod->ncol());
    if (is_sparse) {
        EXPECT_TRUE(sparse_mod->sparse());
    } else {
        EXPECT_FALSE(sparse_mod->sparse());
    }

    auto refvec = this->simulated;
    for (size_t r = 0; r < this->nrow; ++r) {
        for (size_t c = 0; c < this->ncol; ++c) {
            auto& x = refvec[r * this->ncol + c];
            x = (x <= vec[row ? r : c]);
        }
    }
    
    tatami::DenseRowMatrix<double> ref(this->nrow, this->ncol, std::move(refvec));
    quick_test_all(dense_mod.get(), &ref);
    quick_test_all(sparse_mod.get(), &ref);
}

TEST_P(CompareVectorTest, NotEqual) {
    auto param = GetParam();
    bool row = std::get<0>(param);
    bool is_sparse = std::get<1>(param);

    std::vector<double> vec(row ? nrow : ncol);
    if (!is_sparse) {
        fill_default_vector(vec);
    }

    std::shared_ptr<tatami::NumericMatrix> dense_mod, sparse_mod;
    if (row) {
        auto op = tatami::make_DelayedNotEqualVectorHelper<0>(vec);
        dense_mod = tatami::make_DelayedUnaryIsometricOp(this->dense, op);
        sparse_mod = tatami::make_DelayedUnaryIsometricOp(this->sparse, op);
    } else {
        auto op = tatami::make_DelayedNotEqualVectorHelper<1>(vec);
        dense_mod = tatami::make_DelayedUnaryIsometricOp(this->dense, op);
        sparse_mod = tatami::make_DelayedUnaryIsometricOp(this->sparse, op);
    }

    EXPECT_FALSE(dense_mod->sparse());
    EXPECT_EQ(dense->nrow(), dense_mod->nrow());
    EXPECT_EQ(dense->ncol(), dense_mod->ncol());
    if (is_sparse) {
        EXPECT_TRUE(sparse_mod->sparse());
    } else {
        EXPECT_FALSE(sparse_mod->sparse());
    }

    auto refvec = this->simulated;
    for (size_t r = 0; r < this->nrow; ++r) {
        for (size_t c = 0; c < this->ncol; ++c) {
            auto& x = refvec[r * this->ncol + c];
            x = (x != vec[row ? r : c]);
        }
    }
    
    tatami::DenseRowMatrix<double> ref(this->nrow, this->ncol, std::move(refvec));
    quick_test_all(dense_mod.get(), &ref);
    quick_test_all(sparse_mod.get(), &ref);
}

INSTANTIATE_TEST_SUITE_P(
    CompareVector,
    CompareVectorTest,
    ::testing::Combine(
        ::testing::Values(true, false), // add by row, or by column
        ::testing::Values(true, false) // check sparse case
    )
);
