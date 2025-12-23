use actix_web::{get, web, App, HttpResponse, HttpServer, Responder};

struct AppState{
    app_name: String,
}

#[get("/app")]
async fn app_index(data: web::Data<AppState>)->String{
    let app_name = &data.app_name;
    format!("{app_name}")
}

#[get("/")]
async fn index() -> impl Responder {
    HttpResponse::Ok().body("Hello world!")
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| {
        App::new()
            .service(index)
            .app_data(web::Data::new( AppState{
                app_name: String::from("EvalRAG")
            }))
            .service(app_index)

    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}