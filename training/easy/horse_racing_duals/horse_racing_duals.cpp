/*
 * =====================================================================================
 *
 *       Filename:  horse_racing_duals.cpp
 *
 *    Description:  SOLUTION OF THE 'HORSE-RACING DUALS' PUZZLE
 *
 *        Version:  1.0
 *        Created:  10/08/2016 23:08:43
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Dr. Samia Drappeau (SD), drappeau.samia@gmail.com
 *
 * =====================================================================================
 */

#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

int main()
{
    int minimum = 1e5;
    int diff = 0;
    int N;
    cin >> N; cin.ignore();
    // We are going to fill in the list of strenghts sorted.
    vector<int> strenght_horses;
    for (int i = 0; i < N; i++) {
        int Pi;
        cin >> Pi; cin.ignore();
        vector<int>::iterator where;
        where = lower_bound (strenght_horses.begin(),strenght_horses.end(),Pi); 
        strenght_horses.insert(where, Pi); 
    }
    
    for (vector<int>::iterator it=strenght_horses.begin(); it!=strenght_horses.end();){
        int horse1 = *it;
        int horse2 = *(++it);
        minimum = min(abs(horse2 - horse1), minimum);
    }
    cout << minimum << endl;
}
