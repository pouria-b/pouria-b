// Reviewed replacement for the uploaded coursework Sudoku demonstration.
// Original source with its AG/April 2007 header is preserved under original/.
#include <array>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using Board = std::array<std::array<int, 9>, 9>;

bool allowed(const Board& board, int row, int col, int value) {
    for (int i = 0; i < 9; ++i) {
        if (board[row][i] == value || board[i][col] == value) return false;
    }
    for (int r = row / 3 * 3; r < row / 3 * 3 + 3; ++r)
        for (int c = col / 3 * 3; c < col / 3 * 3 + 3; ++c)
            if (board[r][c] == value) return false;
    return true;
}

Board read_board(std::istream& input) {
    Board board{};
    std::string token;
    for (int i = 0; i < 81; ++i) {
        if (!(input >> token) || token.size() != 1 || token[0] < '0' || token[0] > '9')
            throw std::invalid_argument("Expected exactly 81 whitespace-separated digits 0-9; use 0 for empty cells.");
        const int value = token[0] - '0';
        if (value && !allowed(board, i / 9, i % 9, value))
            throw std::invalid_argument("Contradictory clues in row, column, or 3x3 box.");
        board[i / 9][i % 9] = value;
    }
    if (input >> token) throw std::invalid_argument("Extra data after the 81 cells.");
    return board;
}

bool solve(Board& board) {
    int best_row = -1, best_col = -1;
    std::vector<int> best_candidates;
    for (int row = 0; row < 9; ++row) {
        for (int col = 0; col < 9; ++col) {
            if (board[row][col]) continue;
            std::vector<int> candidates;
            for (int value = 1; value <= 9; ++value)
                if (allowed(board, row, col, value)) candidates.push_back(value);
            if (candidates.empty()) return false;
            if (best_row == -1 || candidates.size() < best_candidates.size()) {
                best_row = row; best_col = col; best_candidates = candidates;
            }
        }
    }
    if (best_row == -1) return true;
    for (int value : best_candidates) {
        board[best_row][best_col] = value;
        if (solve(board)) return true;
    }
    board[best_row][best_col] = 0;
    return false;
}

int main(int argc, char* argv[]) {
    try {
        if (argc > 2) throw std::invalid_argument("Usage: sudoku [PUZZLE_FILE]; without a path, read stdin.");
        std::ifstream file;
        if (argc == 2) {
            file.open(argv[1]);
            if (!file) throw std::invalid_argument("Cannot open puzzle file.");
        }
        auto board = read_board(argc == 2 ? static_cast<std::istream&>(file) : std::cin);
        if (!solve(board)) { std::cerr << "No solution.\n"; return 2; }
        for (const auto& row : board) {
            for (int i = 0; i < 9; ++i) std::cout << row[i] << (i == 8 ? '\n' : ' ');
        }
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
    return 0;
}
