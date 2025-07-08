// main.cpp
// PhantomRoll: Ultra-Low-Latency Telegram Dice Sender & Deleter
// Developed for master's level research and production-grade deployment

#include <iostream>
#include <csignal>
#include <cstdlib>
#include <thread>
#include <chrono>

#include "td/telegram/td_json_client.h"
#include "utils/config_loader.hpp"
#include "core/telegram_session.hpp"
#include "core/message_handler.hpp"
#include "core/socket_server.hpp"  // ✅ NEW
#include "nlohmann/json.hpp"

using json = nlohmann::json;
using namespace std;

// Signal handler for graceful shutdown
static void signal_handler(int signal) {
    std::cerr << "\n[INFO] Termination signal (" << signal << ") received. Shutting down PhantomRoll cleanly..." << std::endl;
    TelegramSession::get_instance().close();
    std::exit(signal);
}

int main(int argc, char* argv[]) {
    std::cout << "╔══════════════════════════════════════════════════════════════╗" << std::endl;
    std::cout << "║        幽影掷点 (PhantomRoll)       ║" << std::endl;
    std::cout << "║  Stealth Telegram Dice Controller  ║" << std::endl;
    std::cout << "╚══════════════════════════════════════════════════════════════╝" << std::endl;

    std::signal(SIGINT, signal_handler);
    std::signal(SIGTERM, signal_handler);

    try {
        // Load configuration
        const std::string config_path = "config/tdlib_config.json";
        utils::ConfigLoader config(config_path);
        const auto& settings = config.get();

        if (!settings.contains("api_id") || !settings.contains("api_hash")) {
            throw std::runtime_error("Missing 'api_id' or 'api_hash' in configuration.");
        }

        if (settings["api_id"].get<int>() == 0 || settings["api_hash"].get<std::string>().empty()) {
            throw std::runtime_error("Invalid 'api_id' or empty 'api_hash' in configuration.");
        }

        // Initialize and authenticate Telegram session
        TelegramSession& session = TelegramSession::get_instance();
        session.initialize(settings);
        session.authenticate();

        // Handle authorization phone number
        static bool phone_number_sent = false;

        while (true) {
            std::string raw_update = session.receive(1.0);
            if (raw_update.empty()) continue;

            json update = json::parse(raw_update, nullptr, false);
            if (!update.is_object()) continue;

            std::cout << "[DEBUG] Received update: " << update.dump(2) << std::endl;

            if (update["@type"] == "updateAuthorizationState") {
                auto auth_state = update["authorization_state"];
                std::string state_type = auth_state["@type"];

                if (state_type == "authorizationStateWaitPhoneNumber" && !phone_number_sent) {
                    std::cout << "[INFO] Sending phone number..." << std::endl;
                    session.send(json{
                        {"@type", "setAuthenticationPhoneNumber"},
                        {"phone_number", "+905380678879"}
                    }.dump());
                    phone_number_sent = true;
                }
            }
        }

        // Launch message handler
        MessageHandler handler(session, settings);
        std::thread handler_thread([&handler]() { handler.run(); });

        // 🔁 Start socket server to receive Java UI commands
        SocketServer control_server(8879); // Port 8879 as agreed
        control_server.start([&](const std::string& cmd) {
            if (cmd == "START") {
                std::cout << "[CONTROL] Received START command." << std::endl;
                // Already started by handler.run(); if restart logic is needed, expand here
            } else if (cmd == "STOP") {
                std::cout << "[CONTROL] Received STOP command." << std::endl;
                session.close();
            } else if (cmd == "STATUS") {
                std::cout << "[CONTROL] STATUS: Authorized=" << session.is_authorized() << std::endl;
            } else {
                std::cout << "[CONTROL] Unknown command received: " << cmd << std::endl;
            }
        });

        handler_thread.join();

    } catch (const std::exception& e) {
        std::cerr << "[FATAL ERROR] " << e.what() << std::endl;
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
