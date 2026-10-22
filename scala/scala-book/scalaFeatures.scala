import scala.sys.BooleanProp
import javax.xml.stream.XMLReporter
import javax.swing.InputMap
trait Animal:
  def speak(): Unit

trait HasTail:
  def wagTail(): Unit

class Dog extends Animal, HasTail:
  def speak(): Unit = println("woof")
  def wagTail(): Unit = println("⎞⎜⎛  ⎞⎜⎛")

class Require {
  val name: String = "uyu"

  def support =
    "," + "and"

  def process(info: String, code: InputMap, reporter: XMLReporter): Unit = {
    println("uyu")
  }
}
