#include <iostream>
#include <fstream>

// http://www.usaco.org/index.php?page=viewproblem2&cpid=1253

// g++ -Wall -Wextra -pedantic -g3 -std=c++17 bronze_problem_3.cpp -o main.exe
using std::string;

template<typename... Args>
inline void print(const Args&... args)
{
    ((std::cout << args << ' '), ...) << '\n';
}

inline std::string input()
{
    std::string userInput;
    std::getline(std::cin, userInput);
    return userInput;
}

inline std::string readString()
{
    std::string userInput;
    std::cin >> userInput;
    return userInput;
}

inline int readInt()
{
    std::string str = readString();
    return std::stoi(str);
}

template<typename T>
inline std::string input(const T& prompt)
{
    std::cout << prompt;
    std::string userInput;
    std::getline(std::cin, userInput);
    return userInput;
}

int main (){

    const size_t testCases = readInt();

    for (size_t i = 0; i < testCases; i++)
    {
        input();

        const size_t numLines = readInt();
        const size_t numInputs = readInt();

        print("input/output", numLines, numInputs);

        while (true)
        {
            std::string input;
            std::cin >> input;

            std::string output;
            std::cin >> output;

            print("input/output", input, output);
        } 
    }

    std::cin.get();
}