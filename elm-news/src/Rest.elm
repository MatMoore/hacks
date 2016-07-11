module Rest exposing (..)
import Http

import Json.Decode exposing (..)
import Types exposing (..)
import Task

endpoint: String
endpoint =
    "https://hn.algolia.com/api/v1/search_by_date?tags=story&hitsPerPage=50"

getNews: Cmd Msg
getNews =
    Http.get decodeNews endpoint
        |> Task.perform Failed Succeed
        |> Cmd.map GetNewsResponse

decodeNews: Decoder (List News)
decodeNews = "hits" := (list decodeNewsItem)

decodeNewsItem : Decoder News
decodeNewsItem =
    object1 News
    ("title" := string)
