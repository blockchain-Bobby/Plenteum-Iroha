/**
 * Copyright Soramitsu Co., Ltd. 2017 All Rights Reserved.
 * http://soramitsu.co.jp
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *        http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "module/irohad/ametsuchi/ametsuchi_mocks.hpp"
#include "module/irohad/network/network_mocks.hpp"
#include "module/irohad/validation/validation_mocks.hpp"

#include "framework/test_subscriber.hpp"
#include "synchronizer/impl/synchronizer_impl.hpp"
#include "validation/chain_validator.hpp"

using namespace iroha;
using namespace iroha::model;
using namespace iroha::ametsuchi;
using namespace iroha::synchronizer;
using namespace iroha::validation;
using namespace iroha::network;
using namespace framework::test_subscriber;

using ::testing::Return;
using ::testing::_;
using ::testing::DefaultValue;

TEST(SynchronizerTest, ValidWhenSingleCommitSynchronized) {
  auto chain_validator = std::make_shared<MockChainValidator>();
  auto mutable_factory = std::make_shared<MockMutableFactory>();
  auto block_loader = std::make_shared<MockBlockLoader>();

  auto synchronizer = iroha::synchronizer::SynchronizerImpl(
      chain_validator, mutable_factory, block_loader);
  Block test_block;
  test_block.height = 5;

  DefaultValue<std::unique_ptr<MutableStorage>>::SetFactory(
      &createMockMutableStorage);
  EXPECT_CALL(*mutable_factory, createMutableStorage()).Times(1);

  EXPECT_CALL(*mutable_factory, commit_(_)).Times(1);

  EXPECT_CALL(*chain_validator, validateBlock(test_block, _))
      .WillOnce(Return(true));

  EXPECT_CALL(*block_loader, requestBlocks(_, _)).Times(0);

  auto wrapper =
      make_test_subscriber<CallExact>(synchronizer.on_commit_chain(), 1);
  wrapper.subscribe([&test_block](auto commit) {
    auto block_wrapper = make_test_subscriber<CallExact>(commit, 1);
    block_wrapper.subscribe([&test_block](auto block) {
      // Check commit block
      ASSERT_EQ(block.height, test_block.height);
    });
    ASSERT_TRUE(block_wrapper.validate());
  });

  synchronizer.process_commit(test_block);

  ASSERT_TRUE(wrapper.validate());
}

TEST(SynchronizerTest, ValidWhenBadStorage) {
  auto chain_validator = std::make_shared<MockChainValidator>();
  auto mutable_factory = std::make_shared<MockMutableFactory>();
  auto block_loader = std::make_shared<MockBlockLoader>();

  Block test_block;

  DefaultValue<std::unique_ptr<MutableStorage>>::Clear();
  EXPECT_CALL(*mutable_factory, createMutableStorage()).Times(1);

  EXPECT_CALL(*mutable_factory, commit_(_)).Times(0);

  EXPECT_CALL(*chain_validator, validateBlock(test_block, _)).Times(0);

  EXPECT_CALL(*block_loader, requestBlocks(_, _)).Times(0);

  auto synchronizer = iroha::synchronizer::SynchronizerImpl(
      chain_validator, mutable_factory, block_loader);

  auto wrapper =
      make_test_subscriber<CallExact>(synchronizer.on_commit_chain(), 0);
  wrapper.subscribe();

  synchronizer.process_commit(test_block);

  ASSERT_TRUE(wrapper.validate());
}

TEST(SynchronizerTest, ValidWhenBlockValidationFailure) {
  auto chain_validator = std::make_shared<MockChainValidator>();
  auto mutable_factory = std::make_shared<MockMutableFactory>();
  auto block_loader = std::make_shared<MockBlockLoader>();

  Block test_block;
  test_block.height = 5;
  test_block.sigs.emplace_back();

  DefaultValue<std::unique_ptr<MutableStorage>>::SetFactory(
      &createMockMutableStorage);
  EXPECT_CALL(*mutable_factory, createMutableStorage()).Times(2);

  EXPECT_CALL(*mutable_factory, commit_(_)).Times(1);

  EXPECT_CALL(*chain_validator, validateBlock(test_block, _))
      .WillOnce(Return(false));
  EXPECT_CALL(*chain_validator, validateChain(_, _)).WillOnce(Return(true));

  EXPECT_CALL(*block_loader, requestBlocks(_, _))
      .WillOnce(Return(rxcpp::observable<>::just(test_block)));

  auto synchronizer = iroha::synchronizer::SynchronizerImpl(
      chain_validator, mutable_factory, block_loader);

  auto wrapper =
      make_test_subscriber<CallExact>(synchronizer.on_commit_chain(), 1);
  wrapper.subscribe([&test_block](auto commit) {
    auto block_wrapper = make_test_subscriber<CallExact>(commit, 1);
    block_wrapper.subscribe([&test_block](auto block) {
      // Check commit block
      ASSERT_EQ(block.height, test_block.height);
    });
    ASSERT_TRUE(block_wrapper.validate());
  });

  synchronizer.process_commit(test_block);

  ASSERT_TRUE(wrapper.validate());
}