#include "utils/config_loader.hpp"
#include <fstream>
#include <stdexcept>
#include <nlohmann/json.hpp>

namespace utils {

ConfigLoader::ConfigLoader(const std::string& path) {
    std::ifstream file(path);
    if (!file.is_open()) {
        throw std::runtime_error("Failed to open config file: " + path);
    }

    file >> config_;
}

const nlohmann::json& ConfigLoader::get() const {
    return config_;
}

}
