port module Main exposing (..)

import Test.Day08
import Test.Runner.Node exposing (run, TestProgram)
import Json.Encode exposing (Value)


main : TestProgram
main =
    run emit Test.Day08.suite


port emit : ( String, Value ) -> Cmd msg
