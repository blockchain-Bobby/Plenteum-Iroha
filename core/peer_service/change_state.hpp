/*
Copyright Soramitsu Co., Ltd. 2016 All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/
#ifndef __IROHA_PEER_SERVICE_CHANGE_STATE_HPP__
#define __IROHA_PEER_SERVICE_CHANGE_STATE_HPP__

#include <string>
#include <peer_service/peer_service.hpp>

namespace peer_service{
    namespace change_state{

        // This scope is issue transaction
        namespace transtion {
          // invoke to issue transaction
          void add(const std::string &ip, const peer::Node &);
          void remove(const std::string &ip, const std::string &);
          void setTrust(const std::string &ip, const std::string &, const double &);
          void changeTrust(const std::string &ip, const std::string &, const double &);
          void setActive(const std::string &ip, const std::string &, const bool active);
        }

        // This scope is validation
        namespace validation {
          bool add(const peer::Node &);
          bool remove(const std::string &);
          bool setTrust(const std::string &, const double &);
          bool changeTrust(const std::string &, const double &);
          bool setActive(const std::string &, const bool active);
        }

        // This scope is runtime
        namespace runtime {
          bool add(const peer::Node &);
          bool remove(const std::string &);
          bool setTrust(const std::string &, const double &);
          bool changeTrust(const std::string &, const double &);
          bool setActive(const std::string &, const bool active);
        }
    };
};

#endif //IROHA_MONITOR_HPP
