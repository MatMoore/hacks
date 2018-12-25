import scala.util.Random

case class Game(player: Entity, boss: Entity, bossDamage: Integer = 9) {
  def doTurn(spell: Spell) = {
    copy(player=player.damage(1)).
    startTurn.
      doSpell(spell).
      map(_.startTurn).
      map(_.bossAction)
  }
  def startTurn = {
    val game2 = player.invokeEffects(this)
    val game3 = game2.boss.invokeEffects(game2)
    game3.copy(player = game3.player.updateEffects, boss = game3.boss.updateEffects)
  }
  def doSpell(spell: Spell): Option[Game] = {
    val possibleGame = player.conjure(spell, this)
    possibleGame match {
      case Some (newGame) if newGame.player.isDead => None
      case x => x
    }
  }
  def bossAction = {
    if(boss.isDead) {
      this
    } else {
      copy(player=player.damage(bossDamage))
    }
  }

  def simulate(spells: Seq[Spell]): Option[Game] = {
       spells.foldLeft(Option(this))(
          (game: Option[Game], spell: Spell) =>
            game.flatMap(_.doTurn(spell))
        )
  }

  def playerWins = boss.isDead && !player.isDead
}
trait Effect {
  def affect(game: Game): Game
  def unaffect(player: Entity) = player
}
case class ArmourEffect(amount: Int) extends Effect {
  def affect(game: Game) = game.copy(player=game.player.addArmour(amount))
  override def unaffect(player: Entity) = player.addArmour(0)
}
case class DamageEffect(amount: Int) extends Effect {
  def affect(game: Game) = game.copy(boss=game.boss.damage(amount))
}
case class RechargeEffect(amount: Int) extends Effect {
  def affect(game: Game) = game.copy(player=game.player.recharge(amount))
}
case class LingeringEffect(roundsLeft: Int, effect: Effect) {
  def affect(game: Game) = effect.affect(game)
  override def toString = s"${effect.getClass.getSimpleName} for $roundsLeft rounds"
}
trait Spell {
  def cost: Int
  def cast(game: Game): Game
}
case object MagicMissile extends Spell {
  val cost: Int = 53
  def cast(game: Game) = game.copy(boss=game.boss.damage(4))
}
case object Drain extends Spell {
  val cost = 73
  def cast(game: Game) = game.copy(player=game.player.heal(2), boss=game.boss.damage(2))
}
case object Shield extends Spell {
  val cost = 113
  def cast(game: Game) = {
    val effect = ArmourEffect(7)
    game.copy(player=game.player.addEffect(LingeringEffect(6, effect)))
  }
}
case object Poison extends Spell {
  val cost = 173
  def cast(game: Game) = {
    val effect = DamageEffect(3)
    game.copy(boss=game.boss.addEffect(LingeringEffect(6, effect)))
  }
}
case object Recharge extends Spell {
  val cost = 229
  def cast(game: Game) = {
    val effect = LingeringEffect(5, RechargeEffect(101))
    game.copy(player=game.player.addEffect(effect))
  }
}
case class Entity(
                   armour: Int = 0,
                   inventory: List[Spell] = List(),
                   effects: List[LingeringEffect] = List(),
                   hp: Int,
                   mana: Int = 0) {
  def capDamage(amount: Int) = {
    if (isDead) 0
    else Math.max(1, amount - armour)
  }
  def damage(amount: Int) = this.copy(hp = hp - capDamage(amount))
  def addArmour(amount: Int) = this.copy(armour = amount)
  def recharge(amount: Int) = {
    this.copy(mana = mana + amount)
  }
  def addEffect(effect: LingeringEffect) = this.copy(effects = (effect :: effects))
  def heal(amount: Int) = {
    if (isDead) this
    else this.copy(hp = hp + amount)
  }
  def updateEffects = {
    var ended: Set[Effect] = Set()
    val newPlayer = this.copy(effects = effects.flatMap(
      (effect: LingeringEffect) =>
        if (effect.roundsLeft == 1) {
          ended = ended + effect.effect
          List()
        }
        else {
          List(effect.copy(roundsLeft = effect.roundsLeft - 1))
        }
    ))

    ended.foldLeft(newPlayer)((acc: Entity, effect: Effect) => effect.unaffect(acc))
  }

  // this went horribly wrong...
  def forbiddenSpellsFromEffects = {
    effects.foldLeft(Set[Spell]())(
      (acc: Set[Spell], effect) => effect match {
        case LingeringEffect(x, DamageEffect(_)) if x > 1 => acc + Poison
        case LingeringEffect(x, RechargeEffect(_)) if x > 1 => acc + Recharge
        case LingeringEffect(x, ArmourEffect(_)) if x > 1 => acc + Shield
        case _ => acc
      })
  }

  def conjure(spell: Spell, game: Game) = {
    if(!isDead && mana >= spell.cost) {
      val newPlayer = this.copy(mana=mana - spell.cost)
      Some(spell.cast(game.copy(player = newPlayer)))
    }
    else
      None
  }
  def invokeEffects(game: Game) = effects.foldLeft(game)((game: Game, effect: LingeringEffect) => effect.affect(game))
  def isDead = hp <= 0
  override def toString = {
    val effectString = effects.map("(" + _.toString + ")").mkString(" ")
    s"ARM=$armour HP=$hp MP=$mana" + " " + effectString
  }
}
val allSpells = List(MagicMissile, Drain, Shield, Poison, Recharge)

/*
val testBoss = Entity(hp=14)
val testGame = Game(Entity(hp=10, mana=250, inventory=allSpells), testBoss, bossDamage = 8)
val testGame2 = testGame.doTurn(Recharge).get
val testGame3 = testGame2.doTurn(Shield).get
val testGame4 = testGame3.doTurn(Drain).get
val testGame5 = testGame4.doTurn(Poison).get
val testGame6 = testGame5.doTurn(MagicMissile).get
val blarg1 = Game(Entity(hp=10, mana=250, inventory=allSpells), Entity(hp=10), bossDamage=8)
blarg1.doTurn(Poison)
blarg1.doTurn(Poison).get.doTurn(MagicMissile)
blarg1.simulate(List(Poison, MagicMissile))
*/


def randomSpell(game: Game, spentMana: Integer=0, history: List[Spell]=List()): Option[Int] = {
  val mana = game.player.mana
  val forbidden = game.player.forbiddenSpellsFromEffects ++ game.boss.forbiddenSpellsFromEffects
  val availSpells = allSpells.filter(_.cost <= mana).filterNot(forbidden.contains(_))
  val numAvail = availSpells.length
  if (numAvail <= 0 || spentMana > 1415) None
  else {
    val spell = availSpells(Random.nextInt(numAvail))
    val result = game.doTurn(spell)
    result match {
      case Some(possibleGame) if (possibleGame.playerWins) => {
        //println(possibleGame)
        //println(spell :: history)
        Some(spentMana + spell.cost)
      }
      case Some(possibleGame) if !possibleGame.player.isDead => randomSpell(possibleGame, spentMana + spell.cost, spell :: history)
      case _ => None
    }
  }

}
val boss = Entity(hp=58, mana=0)
val start = Game(player=Entity(inventory=allSpells, hp=50, mana=500), boss=boss)
val fuckit = start.simulate(List(Poison, Recharge, Shield)).get
(1 to 1000000).map(i => randomSpell(fuckit, spentMana = Poison.cost + Shield.cost + Recharge.cost)).flatten.min
