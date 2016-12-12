module Main exposing (..)

import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import WebSocket
import Json.Decode exposing (Decoder, field)
import Json.Encode
import Debug exposing (log)


type alias Point =
    { x : Float
    , y : Float
    }


type alias Reading =
    { distance : Float
    , position : Point
    }


type alias Player =
    { name : String
    , position : Vector
    }


type alias Response =
    { gpss : List Reading
    , players : List Player
    }


decodePoint : Decoder Point
decodePoint =
    Json.Decode.map2 Point
        (Json.Decode.field "x" Json.Decode.float)
        (Json.Decode.field "y" Json.Decode.float)


decodeReading : Decoder Reading
decodeReading =
    Json.Decode.map2 Reading
        (Json.Decode.field "distance" Json.Decode.float)
        (Json.Decode.field "position" decodePoint)


decodePlayer : Decoder Player
decodePlayer =
    Json.Decode.map2 Player
        (Json.Decode.field "name" Json.Decode.string)
        (Json.Decode.field "position" decodePoint)


decodeResponse : Decoder Response
decodeResponse =
    Json.Decode.map2 Response
        (Json.Decode.field "gpss" (Json.Decode.list decodeReading))
        (Json.Decode.field "players" (Json.Decode.list decodePlayer))


example =
    """{
  "gpss":[
  {
    "distance":18.601075237738275,
    "position":{"x":-10,"y":-8}
  },
  {
    "distance":10.63014581273465,
    "position":{"x":12,"y":-5}
  },
  {
    "distance":10.816653826391969,"position":{"x":-4,"y":9}
  }
],
    "sampleCommands":[
    {"tag":"SetName","contents":"Kris"},
    {"tag":"SetColor","contents":"#ff0000"},
    {"tag":"Move","contents":{"x":1,"y":-2}}
    ],
    "players":[
    {"color":null,"score":0,
    "name":"<Your Name Here>","position":{"x":0,"y":0}
    }]
}
"""


readingToCircle reading =
    { x = reading.position.x, y = reading.position.y, r = reading.distance }


readingIntersection : List Reading -> Result String Vector
readingIntersection readings =
    case readings of
        first :: second :: rest ->
            Ok (intersectionPoint (readingToCircle first) (readingToCircle second))
                |> Result.map (\(Intersection point1 point2) -> point1)

        _ ->
            Err "Wrong number of readings"


type Request
    = SetName String
    | SetColor String
    | Move Vector


type alias Vector =
    { x : Float, y : Float }


encodeVector : Vector -> Json.Encode.Value
encodeVector vector =
    Json.Encode.object
        [ ( "x", Json.Encode.float vector.x )
        , ( "y", Json.Encode.float vector.y )
        ]


encodeRequest : Request -> Json.Encode.Value
encodeRequest request =
    case request of
        SetName string ->
            Json.Encode.object
                [ ( "tag", (Json.Encode.string "SetName") )
                , ( "contents", (Json.Encode.string string) )
                ]

        SetColor colour ->
            Json.Encode.object
                [ ( "tag", (Json.Encode.string "SetColor") )
                , ( "contents", (Json.Encode.string colour) )
                ]

        Move direction ->
            Json.Encode.object
                [ ( "tag", (Json.Encode.string "Move") )
                , ( "contents", encodeVector direction )
                ]


type Intersection
    = Intersection Vector Vector


type alias Circle =
    { x : Float, y : Float, r : Float }



-- intersection : Circle -> Circle -> Maybe Intersection
-- intersection =


intersectionPoint c1 c2 =
    let
        d =
            sqrt ((c1.x - c2.x) * (c1.x - c2.x) + (c1.y - c2.y) * (c1.y - c2.y))

        l =
            ((c1.r * c1.r) - (c2.r * c2.r) + d * d) / (2 * d)

        h =
            sqrt (c1.r * c1.r - l * l)

        x1 =
            (l / d) * (c2.x - c1.x) + (h / d) * (c2.y - c1.y) + c1.x

        y1 =
            (l / d) * (c2.y - c1.y) - (h / d) * (c2.x - c1.x) + c1.y

        x2 =
            (l / d) * (c2.x - c1.x) - (h / d) * (c2.y - c1.y) + c1.x

        y2 =
            (l / d) * (c2.y - c1.y) + (h / d) * (c2.x - c1.x) + c1.y
    in
        Intersection (Vector x1 y1) (Vector x2 y2)


main : Program Never Model Msg
main =
    Html.program
        { init = init
        , view = view
        , update = update
        , subscriptions = subscriptions
        }


echoServer : String
echoServer =
    "ws://game.clearercode.com/"


type alias Model =
    { input : String
    , messages : List String
    }


init : ( Model, Cmd Msg )
init =
    ( Model "" [], Cmd.batch [ sendRequest (SetName "Not a bot!"), sendRequest (SetColor "red") ] )


type Msg
    = Input String
    | Send
    | NewMessage String


findLocation : List Player -> Maybe Vector
findLocation players =
    List.filter (\player -> player.name == "Not a bot!") players
        |> List.map .position
        |> List.head


sendRequest : Request -> Cmd Msg
sendRequest request =
    encodeRequest request
        |> Json.Encode.encode 2
        |> WebSocket.send echoServer


relativeTo : Vector -> Vector -> Vector
relativeTo origin vector =
    { x = vector.x - origin.x, y = vector.y - origin.y }


update : Msg -> Model -> ( Model, Cmd Msg )
update msg { input, messages } =
    case msg of
        Input newInput ->
            ( Model newInput messages, Cmd.none )

        Send ->
            ( Model "" messages, WebSocket.send echoServer input )

        NewMessage str ->
            case Json.Decode.decodeString decodeResponse str of
                Ok { gpss, players } ->
                    let
                        target =
                            readingIntersection gpss

                        location =
                            findLocation players |> Maybe.withDefault { x = 0, y = 0 }

                        cmd =
                            case Result.map (relativeTo location) target of
                                Ok someTarget ->
                                    sendRequest (Move someTarget)

                                Err msg ->
                                    Cmd.none
                    in
                        ( Model input (str :: messages), cmd )

                _ ->
                    ( Model input (str :: messages), Cmd.none )


subscriptions : Model -> Sub Msg
subscriptions model =
    WebSocket.listen echoServer NewMessage


view : Model -> Html Msg
view model =
    div []
        [ input [ onInput Input, value model.input ] []
        , button [ onClick Send ] [ text "Send" ]
        , div [] (List.map viewMessage (List.reverse model.messages))
        ]


viewMessage : String -> Html msg
viewMessage msg =
    div [] [ text msg ]
