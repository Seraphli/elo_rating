namespace py ratingserver

service rating_server {
    void ping()
    string version()
    void set_result(1:string player_1, 2:string player_2, 3:i8 result, 4:string game_id)
    void set_rating(1:string player, 2:i16 rating)
    i16 get_rating(1:string player)
    string leadboard(1:i8 number)
}
