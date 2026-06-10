trait Animal:
  def speak(): Unit

trait HasTail:
  def wagTail(): Unit

class Dog extends Animal, HasTail:
  def speak(): Unit = println("woof")
  def wagTail(): Unit = println("⎞⎜⎛  ⎞⎜⎛")


