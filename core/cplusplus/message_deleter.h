#ifndef MESSAGE_DELETER_H
#define MESSAGE_DELETER_H

#include <string>
#include <vector>
#include <cstdint>

class MessageDeleter {
public:
    MessageDeleter(const std::string& sessionPath);
    ~MessageDeleter();

    // Initializes connection to Telegram API via native bindings (future)
    bool initialize();

    // Deletes a message given chat ID and message ID
    bool deleteMessage(int64_t chat_id, int32_t message_id);

    // Deletes multiple messages
    bool deleteMessages(int64_t chat_id, const std::vector<int32_t>& message_ids);

private:
    std::string session_path_;
    bool initialized_;

    // Internal method to simulate or trigger deletion
    bool performDeletion(int64_t chat_id, int32_t message_id);
};

#endif // MESSAGE_DELETER_H
