// Copyright (c) 2022 MIT License by 6.172 / 6.106 Staff

////////////////////////////////////////////////////////////////////////////
//
// listi.h
//
// CListIterator<class T> template definition
//
// Remi Coulom
//
// june 1996
//
////////////////////////////////////////////////////////////////////////////
#ifndef LISTI_H
#define LISTI_H

#include "./list.h"       // CList template

////////////////////////////////////////////////////////////////////////////
// CListIterator class definition
////////////////////////////////////////////////////////////////////////////
template<class T>
class CListIterator {  // listi
 private:  //////////////////////////////////////////////////////////////////
  CList<T>* plt;
  CListCell<T>* pcellCurrent;
  CListCell<T>* pcellPrevious;

 public:  ///////////////////////////////////////////////////////////////////
  CListIterator(CList<T>& ltInit);

  void Increment();
  void Remove();
  void Insert();
  void Reset();

  T& Value();
  int IsFirst() const {
    return !pcellPrevious;
  }
  int IsAtTheEnd() const {
    return !pcellCurrent;
  }
};

////////////////////////////////////////////////////////////////////////////
// Constructor
////////////////////////////////////////////////////////////////////////////
template<class T>
CListIterator<T>::CListIterator(CList<T>& ltInit) {
  plt = &ltInit;
  pcellPrevious = 0;
  pcellCurrent = ltInit.pcellFirst;
}

////////////////////////////////////////////////////////////////////////////
// Resets an iterator to the beginning of its list
////////////////////////////////////////////////////////////////////////////
template<class T>
void CListIterator<T>::Reset() {
  pcellPrevious = 0;
  pcellCurrent = plt->pcellFirst;
}

////////////////////////////////////////////////////////////////////////////
// Moves to the next position in a list
////////////////////////////////////////////////////////////////////////////
template<class T>
INLINE
void CListIterator<T>::Increment() {
  ASSERT(!IsAtTheEnd());
  pcellPrevious = pcellCurrent;
  pcellCurrent = pcellCurrent->Next();
}

////////////////////////////////////////////////////////////////////////////
// Insert one cell at the current position
////////////////////////////////////////////////////////////////////////////
template<class T>
void CListIterator<T>::Insert() {
  if (!pcellPrevious) {
    plt->Add();
    pcellCurrent = plt->pcellFirst;
  } else {
    CListCell<T>* pcellNew = plt->AllocateCell();
    pcellNew->Link(pcellCurrent);
    pcellPrevious->Link(pcellNew);
    pcellCurrent = pcellNew;
  }
}

////////////////////////////////////////////////////////////////////////////
// Removes one cell from the list
////////////////////////////////////////////////////////////////////////////
template<class T>
void CListIterator<T>::Remove() {
  ASSERT(!IsAtTheEnd());

  {
    CListCell<T>* pcell = pcellCurrent;
    pcellCurrent = pcellCurrent->Next();
    plt->FreeCell(pcell);
  }

  if (pcellPrevious) {
    pcellPrevious->Link(pcellCurrent);
  } else {
    plt->pcellFirst = pcellCurrent;
  }
}

////////////////////////////////////////////////////////////////////////////
// Reads the value contained by the current cell
////////////////////////////////////////////////////////////////////////////
template<class T>
INLINE
T& CListIterator<T>::Value() {
  ASSERT(!IsAtTheEnd());
  return pcellCurrent->Value();
}

#endif  // LISTI_H