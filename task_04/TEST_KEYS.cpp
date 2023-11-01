#include <iostream>
#include <vector>
#include <unordered_map>
#include <string>
#include <Windows.h>

using namespace std;

bool monobitTest(const vector<int>& sequence) {
    int onesCount = 0;
    int zerosCount = 0;

    // Підрахунок кількості одиниць та нулів у послідовності
    for (int bit : sequence) {
        if (bit == 1) onesCount++;
        else zerosCount++;   
    }

    // Константи зі стандарту FIPS-140 для порівняння
    const int lowerBound = 9654;
    const int upperBound = 10346;

    // Порівняння з константами
    if (onesCount >= lowerBound && onesCount <= upperBound &&
        zerosCount >= lowerBound && zerosCount <= upperBound) {
        return true;
    }

    return false;
}

bool maxSeriesLengthTest(const vector<int>& sequence) {
    int maxZeroSeries = 0;
    int maxOneSeries = 0;
    int currentZeroSeries = 0;
    int currentOneSeries = 0;

    for (int bit : sequence) {
        if (bit == 0) {
            currentZeroSeries++;
            currentOneSeries = 0;
            if (currentZeroSeries > maxZeroSeries) maxZeroSeries = currentZeroSeries;
        }
        else {
            currentOneSeries++;
            currentZeroSeries = 0;
            if (currentOneSeries > maxOneSeries) maxOneSeries = currentOneSeries;
        }
    }

    // Максимально припустима довжина серії згідно зі стандартом FIPS-140
    const int maxSeriesLength = 36;

    // Перевірка, чи довжина найдовшої серії в межах допустимого значення
    if (maxZeroSeries <= maxSeriesLength && maxOneSeries <= maxSeriesLength) return true;

    return false;
}

bool pokerTest(const vector<int>& sequence) {
    // Розмір блоку Поккера (згідно з вимогами)
    const int blockSize = 4;

    // Розділення послідовності на блоки
    vector<vector<int>> blocks;
    for (int i = 0; i < sequence.size(); i += blockSize) {
        vector<int> block;
        for (int j = 0; j < blockSize && i + j < sequence.size(); j++) block.push_back(sequence[i + j]);

        blocks.push_back(block);
    }

    // Підрахунок кількості кожного блоку
    unordered_map<string, int> blockCounts;
    for (const vector<int>& block : blocks) {
        string blockString;
        for (int bit : block) blockString += to_string(bit);
        
        blockCounts[blockString]++;
    }

    // Розрахунок параметра X3 (кількість блоків, які зустрічаються r раз)
    double X3 = 0.0;
    for (const auto& entry : blockCounts) X3 += entry.second * entry.second;
    
    X3 = (X3 * 16.0 / blocks.size()) - 5000;

    // Межі допустимого X3 згідно зі стандартом FIPS-140
    const double lowerBound = 1.03;
    const double upperBound = 57.4;

    // Перевірка, чи X3 потрапляє в діапазон
    if (X3 >= lowerBound && X3 <= upperBound)  return true;
    
    return false;
}

bool seriesLengthTest(const vector<int>& sequence) {
    // Ініціалізуємо лічильники для кількості серій одиниць та нулів різної довжини
    vector<int> onesCounts(7, 0);
    vector<int> zerosCounts(7, 0);

    int currentCount = 1;
    int currentBit = sequence[0];

    // Перевіряємо кожен біт у послідовності
    for (size_t i = 1; i < sequence.size(); i++) {
        if (sequence[i] == currentBit) currentCount++;
        else {
            // Перевіряємо серію, якщо це зміна біта
            if (currentBit == 0) {
                if (currentCount >= 6) zerosCounts[6]++;
                else zerosCounts[currentCount - 1]++;
            }
            else {
                if (currentCount >= 6) onesCounts[6]++;
                else onesCounts[currentCount - 1]++;
            }
            // Скидаємо лічильник
            currentCount = 1;
            currentBit = sequence[i];
        }
    }

    // Перевіряємо останню серію
    if (currentBit == 0) {
        if (currentCount >= 6) zerosCounts[6]++;
        else zerosCounts[currentCount - 1]++;
    }
    else {
        if (currentCount >= 6) onesCounts[6]++;
        else onesCounts[currentCount - 1]++;
    }

    // Межі допустимих кількостей серій згідно зі стандартом FIPS-140
    const int onesLowerBound[7] = { 2267, 1079, 502, 223, 90, 90, 90 };
    const int onesUpperBound[7] = { 2733, 1421, 748, 402, 223, 223, 223 };
    const int zerosLowerBound[7] = { 2267, 1079, 502, 223, 90, 90, 90 };
    const int zerosUpperBound[7] = { 2733, 1421, 748, 402, 223, 223, 223 };

    for (int i = 0; i < 7; i++) {
        if ((onesCounts[i] < onesLowerBound[i]) || (onesCounts[i] > onesUpperBound[i]) ||
            (zerosCounts[i] < zerosLowerBound[i]) || (zerosCounts[i] > zerosUpperBound[i])) {
            return false;
        }
    }

    return true;
}

// Функція для генерації випадкової послідовності бітів
vector<int> generateRandomSequence(int length) {
    vector<int> sequence;
    srand(static_cast<unsigned>(time(0))); // Ініціалізація генератора випадкових чисел за поточним часом

    for (int i = 0; i < length; i++) {
        int bit = rand() % 2; // Генерувати випадковий біт (0 або 1)
        sequence.push_back(bit);
    }

    return sequence;
}

int main() {
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);

    int sequenceLength = 20000;
    vector<int> sequence1 = generateRandomSequence(sequenceLength);

    // Монобытний тест
    if (monobitTest(sequence1)) cout << "Послідовність вважається випадковою за монобітним тестом." << endl;
    else cout << "Послідовність не вважається випадковою за монобітним тестом." << endl;

    // Тест максимальної довжини серії
    if (maxSeriesLengthTest(sequence1)) cout << "Послідовність вважається випадковою за тестом максимальної довжини серії." << endl;
    else cout << "Послідовність не вважається випадковою за тестом максимальної довжини серії." << endl;

    // Тест Поккера
    if (pokerTest(sequence1)) cout << "Послідовність вважається випадковою за тестом Поккера." << endl;
    else cout << "Послідовність не вважається випадковою за тестом Поккера." << endl;

    // Тест довжин серії
    if (seriesLengthTest(sequence1)) cout << "Послідовність вважається випадковою за тестом довжин серій." << endl;
    else cout << "Послідовність не вважається випадковою за тестом довжин серій." << endl;

    return 0;
}

