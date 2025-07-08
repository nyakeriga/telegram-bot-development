// telegram_session.cpp
// TDLib Session Manager Implementation
// Developed for PhantomRoll stealth dice automation

#include "telegram_session.hpp"
#include <td/telegram/td_json_client.h>
#include <nlohmann/json.hpp>
#include <iostream>
#include <stdexcept>
#include <cstring>
#include <cstdlib>
#include <ctime>

using namespace std;

TelegramSession::TelegramSession() {
    client_ = td_json_client_create();
    authorized_ = false;
    running_ = true;
    std::srand(static_cast<unsigned int>(std::time(nullptr))); // Seed for random jitter
}

TelegramSession::~TelegramSession() {
    close();
    if (client_) {
        td_json_client_destroy(client_);
    }
}

TelegramSession& TelegramSession::get_instance() {
    static TelegramSession instance;
    return instance;
}

void TelegramSession::initialize(const nlohmann::json& config) {
    config_ = config;
    std::cout << "[DEBUG] api_id: " << config_.at("api_id") << std::endl;
    std::cout << "[DEBUG] api_hash: " << config_.at("api_hash").get<std::string>() << std::endl;
}

void TelegramSession::authenticate() {
    // ✅ Validation for api_id/api_hash before proceeding
    if (!config_.contains("api_id") || !config_.contains("api_hash") ||
        config_["api_id"].get<int>() == 0 || config_["api_hash"].get<std::string>().empty()) {
        throw std::runtime_error("Invalid or missing api_id/api_hash in config.");
    }

    while (!authorized_) {
        string response = receive();
        if (response.empty()) continue;

        auto json = nlohmann::json::parse(response, nullptr, false);
        if (!json.is_object()) continue;

        string type = json["@type"];
        if (type == "updateAuthorizationState") {
            string state = json["authorization_state"]["@type"];

            if (state == "authorizationStateWaitTdlibParameters") {
                nlohmann::json request = {
                    {"@type", "setTdlibParameters"},
                    {"database_directory", config_.at("database_directory").get<std::string>()},
                    {"use_message_database", config_.at("use_message_database").get<bool>()},
                    {"use_secret_chats", config_.at("use_secret_chats").get<bool>()},
                    {"api_id", config_.at("api_id").get<int>()},
                    {"api_hash", config_.at("api_hash").get<std::string>()},
                    {"system_language_code", config_.at("system_language_code").get<std::string>()},
                    {"device_model", config_.at("device_model").get<std::string>()},
                    {"system_version", config_.at("system_version").get<std::string>()},
                    {"application_version", config_.at("application_version").get<std::string>()},
                    {"enable_storage_optimizer", true},
                    {"use_test_dc", config_.at("use_test_dc").get<bool>()},
                    {"ignore_file_names", true}
                };

                send(request.dump());

            } else if (state == "authorizationStateWaitPhoneNumber") {
                cout << "[AUTH] Enter your phone number: ";
                string phone;
                getline(cin, phone);
                send(nlohmann::json{
                    {"@type", "setAuthenticationPhoneNumber"},
                    {"phone_number", phone}
                }.dump());

            } else if (state == "authorizationStateWaitCode") {
                cout << "[AUTH] Enter the code you received: ";
                string code;
                getline(cin, code);
                send(nlohmann::json{
                    {"@type", "checkAuthenticationCode"},
                    {"code", code}
                }.dump());

            } else if (state == "authorizationStateReady") {
                cout << "[AUTH] ✅ Authorization successful.\n";
                authorized_ = true;

            } else if (state == "authorizationStateClosed") {
                throw runtime_error("Authorization closed unexpectedly.");
            }

        } else if (type == "error") {
            cerr << "[ERROR] " << json.dump(2) << endl;
        }
    }

    run_async_listener();
}

void TelegramSession::run_async_listener() {
    listener_thread_ = std::thread([this]() {
        while (running_) {
            string update = receive(1.0);
            if (!update.empty()) {
                cout << "[TDLib Update] " << update << endl;

                if (update.find("messageDice") != std::string::npos) {
                    int base_delay = config_.value("delete_delay_ms", 100);
                    int jitter = std::rand() % 20 + 5; // 5–24 ms jitter
                    int final_delay = base_delay + jitter;
                    std::this_thread::sleep_for(std::chrono::milliseconds(final_delay));
                }
            }
        }
    });
}

void TelegramSession::send(const std::string& request) {
    lock_guard<mutex> lock(send_mutex_);
    td_json_client_send(client_, request.c_str());
}

std::string TelegramSession::receive(double timeout) {
    const char* result = td_json_client_receive(client_, timeout);
    if (result) {
        std::string raw(result);
        std::cout << "[RAW RECEIVE] " << raw << std::endl;  // ← ✅ Debug print added
        return raw;
    }
    return "";
}

void TelegramSession::close() {
    running_ = false;
    if (listener_thread_.joinable()) listener_thread_.join();
    send(R"({"@type":"close"})");
}

bool TelegramSession::is_authorized() const {
    return authorized_;
}
