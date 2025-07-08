// message_handler.hpp
// Handles dice message filtering and deletion
// Part of PhantomRoll stealth automation system

#ifndef PHANTOMROLL_MESSAGE_HANDLER_HPP
#define PHANTOMROLL_MESSAGE_HANDLER_HPP

#include <nlohmann/json.hpp>
#include "telegram_session.hpp"

class MessageHandler {
public:
    MessageHandler(TelegramSession& session, const nlohmann::json& config);
    void run();

private:
    TelegramSession& session_;
    nlohmann::json config_;

    void handle_update(const nlohmann::json& update);
    bool is_dice_message(const nlohmann::json& message);
    void delete_message(const nlohmann::json& message);
};

#endif // PHANTOMROLL_MESSAGE_HANDLER_HPP
