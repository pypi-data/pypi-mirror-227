#include <pybind11/pybind11.h>
#include <iostream>
using namespace std;

void printSei(void){
  cout << "I Love Sei zz" << endl;
  return;
}


PYBIND11_MODULE(SEILOV, m){
  m.def("printSei", &printSei, "print I Love Sei zz");
}

