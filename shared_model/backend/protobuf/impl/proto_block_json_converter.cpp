/**
 * Copyright Soramitsu Co., Ltd. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */

#include "backend/protobuf/proto_block_json_converter.hpp"

#include <google/protobuf/util/json_util.h>
#include <string>

#include "backend/protobuf/block.hpp"

using namespace shared_model;
using namespace shared_model::proto;

iroha::expected::Result<interface::types::JsonType, std::string>
ProtoBlockJsonConverter::serialize(const interface::Block &block) const
    noexcept {
  const auto &proto_block = static_cast<const Block &>(block).getTransport();
  std::string result;
  auto status =
      google::protobuf::util::MessageToJsonString(proto_block, &result);

  if (not status.ok()) {
    return iroha::expected::makeError(status.error_message());
  }
  return iroha::expected::makeValue(result);
}

iroha::expected::Result<std::unique_ptr<interface::Block>, std::string>
ProtoBlockJsonConverter::deserialize(
    const interface::types::JsonType &json) const noexcept {
  iroha::protocol::Block block;
  auto status = google::protobuf::util::JsonStringToMessage(json, &block);
  if (not status.ok()) {
    return iroha::expected::makeError(status.error_message());
  }
  std::unique_ptr<interface::Block> result =
      std::make_unique<Block>(std::move(block));
  return iroha::expected::makeValue(std::move(result));
}
