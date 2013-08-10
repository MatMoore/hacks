package s99

import Solutions._

trait ListsSolutions {

  def last[T](list: List[T]): T = list.reduceLeft((a: T, b: T) => b)

  def penultimate[T](list: List[T]): T = list match {
    case head :: (head2 :: Nil) => head
    case head :: (head2 :: tail2) => penultimate(head2 :: tail2)
    case _ => throw new NoSuchElementException
  }

  def nth[T](n: Int, list: List[T]): T = {
    if (n == 0) {
      list.head
    } else if (n < 0) {
      throw new NoSuchElementException
    } else {
      nth(n - 1, list.tail)
    }
  }

  def length[T](list: List[T]): Int = list.foldLeft[Int](0)((count : Int, _ : T) => count + 1)

  def reverse[T](list: List[T]): List[T] = list match {
    case head :: Nil => head :: Nil
    case head :: tail => reverse(tail) :+ head
    case _ => Nil
  }

  def isPalindrome[T](list: List[T]): Boolean = reverse(list) == list

  def flatten(list: List[Any]): List[Any] = list match {
    case (head : List[Any]) :: tail => flatten(head) ++ flatten(tail)
    case head :: tail => head :: flatten(tail)
    case Nil => Nil
  }

  def compress[T](list: List[T]): List[T] = ???
  def pack[T](list: List[T]): List[List[T]] = ???
  def encode[T](list: List[T]): List[(Int, T)] = ???
  def encodeModified[T](list: List[T]): List[Any] = ???
  def decode[T](list: List[(Int, T)]): List[T] = ???
  def encodeDirect[T](list: List[T]): List[(Int, T)] = ???
  def duplicate[T](list: List[T]): List[T] = ???
  def duplicateN[T](n: Int, list: List[T]): List[T] = ???
  def drop[T](n: Int, list: List[T]): List[T] = ???
  def split[T](n: Int, list: List[T]): (List[T], List[T]) = ???
  def slice[T](i: Int, j: Int, list: List[T]): List[T] = ???
  def rotate[T](n: Int, list: List[T]): List[T] = ???
  def removeAt[T](i: Int, list: List[T]): (List[T], T) = ???
  def insertAt[T](t: T, i: Int, list: List[T]): List[T] = ???
  def range[T](i: Int, j: Int): List[Int] = ???
  def randomSelect[T](n: Int, list: List[T]): List[T] = ???
  def lotto[T](i: Int, j: Int): List[Int] = ???
  def randomPermute[T](list: List[T]): List[T] = ???
  def combinations[T](n: Int, list: List[T]): List[List[T]] = ???
  def group3[T](list: List[T]): List[List[List[T]]] = ???
  def groups[T](ns: List[Int], list: List[T]): List[List[List[T]]] = ???
  def lsort[T](list: List[List[T]]): List[List[T]] = ???
  def lsortFreq[T](list: List[List[T]]): List[List[T]] = ???

}

