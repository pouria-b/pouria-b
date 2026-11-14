// Educational 3x3 Hill Cipher encryption over A-Z, modulo 26.
#include <array>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>

using Matrix = std::array<std::array<int, 3>, 3>;

std::string letters(std::string text) {
    for (char& c : text) {
        if (c >= 'a' && c <= 'z') c = static_cast<char>(c - 'a' + 'A');
        if (c < 'A' || c > 'Z') throw std::invalid_argument("Use ASCII letters A-Z only; spaces and punctuation are not accepted.");
    }
    return text;
}

Matrix key_matrix(const std::string& raw) {
    if (raw.size() != 9) throw std::invalid_argument("Key must contain exactly 9 letters.");
    const auto key = letters(raw);
    Matrix m{};
    for (int i = 0; i < 9; ++i) m[i / 3][i % 3] = key[i] - 'A';
    const int det = m[0][0] * (m[1][1]*m[2][2] - m[1][2]*m[2][1])
                  -m[0][1] * (m[1][0]*m[2][2] - m[1][2]*m[2][0])
                  +m[0][2] * (m[1][0]*m[2][1] - m[1][1]*m[2][0]);
    if (std::gcd((det % 26 + 26) % 26, 26) != 1)
        throw std::invalid_argument("Key matrix must be invertible modulo 26 (gcd(det, 26) = 1).");
    return m;
}

std::string encrypt(const std::string& raw, const Matrix& key) {
    if (raw.empty() || raw.size() % 3 != 0)
        throw std::invalid_argument("Message length must be a positive multiple of 3; no padding is added.");
    const auto message = letters(raw);
    std::string result;
    result.reserve(message.size());
    for (std::size_t start = 0; start < message.size(); start += 3) {
        for (int row = 0; row < 3; ++row) {
            int value = 0;
            for (int col = 0; col < 3; ++col) value += key[row][col] * (message[start + col] - 'A');
            result += static_cast<char>('A' + value % 26);
        }
    }
    return result;
}

int main(int argc, char* argv[]) {
    try {
        if (argc == 3) {
            std::cout << encrypt(argv[2], key_matrix(argv[1])) << '\n';
            return 0;
        }
        if (argc != 1) throw std::invalid_argument("Usage: hill_cipher [NINE_LETTER_KEY MESSAGE]");
        std::cout << "Key (9 letters): ";
        std::string key;
        if (!std::getline(std::cin, key)) return 0;
        const auto matrix = key_matrix(key);
        std::string message;
        while (std::cout << "Message (multiple of 3 letters; !!! to quit): ", std::getline(std::cin, message)) {
            if (message == "!!!") break;
            try { std::cout << encrypt(message, matrix) << '\n'; }
            catch (const std::invalid_argument& error) { std::cerr << error.what() << '\n'; }
        }
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
    return 0;
}
