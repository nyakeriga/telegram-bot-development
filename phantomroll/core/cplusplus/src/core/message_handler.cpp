#include "core/message_handler.hpp"
#include <iostream>
#include <thread>
#include <chrono>
#include <sstream>

using namespace std;

MessageHandler::MessageHandler(TelegramSession& session, const nlohmann::json& config)
    : session_(session), config_(config) {}

void MessageHandler::run() {
    std::thread([this]() { send_dice_and_delete_loop(); }).detach();
    std::cout << "[INFO] PhantomRoll dice handler started." << std::endl;
    while (session_.is_authorized()) {
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
}

void MessageHandler::send_dice_and_delete_loop() {
    const auto chat_id = config_["target_chat_id"].get<int64_t>();
    const auto emoji = config_["dice_emoji"].get<std::string>();
    const int interval_ms = config_.value("interval_ms", 3000);

    while (session_.is_authorized()) {
        std::string dice_request = build_dice_message(emoji);
        session_.send(dice_request);

        std::string response = session_.receive(5.0);
        if (!response.empty()) {
            auto json = nlohmann::json::parse(response, nullptr, false);
            if (json.is_discarded()) continue;

            if (json.contains("result") && json["result"].contains("message")) {
                auto msg = json["result"]["message"];
                if (msg.contains("id")) {
                    int64_t message_id = msg["id"];
                    std::this_thread::sleep_for(std::chrono::milliseconds(500));
                    delete_message(chat_id, message_id);
                }
            }
        }

        std::this_thread::sleep_for(std::chrono::milliseconds(interval_ms));
    }
}

std::string MessageHandler::build_dice_message(const std::string& emoji) {
    std::ostringstream ss;
    ss << R"({
        "@type": "sendMessage",
        "chat_id": )" << config_["target_chat_id"] << R"(,
        "input_message_content": {
            "@type": "inputMessageDice",
            "emoji": ")" << emoji << R"("
        }
    })";
    return ss.str();
}

void MessageHandler::delete_message(int64_t chat_id, int64_t message_id) {
    if (message_id <= 0) return;  // Ensure valid message ID
    std::ostringstream ss;
    ss << R"({
        "@type": "deleteMessages",
        "chat_id": )" << chat_id << R"(,
        "message_ids": [)" << message_id << R"(],
        "revoke": true
    })";
    session_.send(ss.str());
}
