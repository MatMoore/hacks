module State exposing (..)
import Types exposing (..)
import Rest exposing (..)

init : ( Model, Cmd Msg )
init = ( {news = Loading}
        , getNews
    )

update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case (Debug.log "OH HI" msg) of
        GetNewsResponse (Err errorMessage) ->
            ( { model | news = Failed errorMessage }, Cmd.none )
        GetNewsResponse (Result.Ok news) ->
            ( { model | news = Succeed news }, Cmd.none )
        Nope ->
            ( model, Cmd.none )

subscriptions : Model -> Sub Msg
subscriptions _ =
    Sub.none
