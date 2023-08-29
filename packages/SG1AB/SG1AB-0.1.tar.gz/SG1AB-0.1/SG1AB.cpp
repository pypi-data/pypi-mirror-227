#include <pybind11/pybind11.h>
#include <iostream>
using namespace std;

void printName(void){
  cout << "Hello We are SG1AB" << endl;
  return;
}


PYBIND11_MODULE(SG1AB, m){
  m.def("printName", &printName, "print Hello We are SG1AB");
}

