var express = require("express");
var app = express();

var port = process.env.PORT || 8080;

const fetch = require("node-fetch");
// const { json } = require("body-parser");
// const { type } = require("os");

var base_url= new URL("https://hatchways.io/api/assessment/blog/posts")

app.get("/api/ping", (req, res) => {
    res.status(200).json({ success:true })
});

// API with correct solution https://hatchways.io/api/assessment/solution/posts?tags=history,tech&sortBy=likes&direction=desc
//Do not call this API in the Application

async function getPosts(url, tag) {
    var url = base_url
    params = {tag:tag}
    url.search = new URLSearchParams(params).toString();
    let res = await fetch(url);
    let data = await res.json()
    return data.posts;
}

app.get('/api/posts', (req, res) => {

    // for (const key in req.query) {
    //     if (req.query.hasOwnProperty(key)){
    //         console.log(key, req.query[key])
    //     }
    // }

    var test = [];
    // var tags = req.query.tags.split(/\s*,\s*/);
    req.query.tags.split(/\s*,\s*/).forEach(function (tag) {

        var url = base_url
        params = {tag:tag}
        url.search = new URLSearchParams(params).toString();

        fetch(url)
            .then(res => {
                return res.json();
            })
            .then(data => data.posts)
            .then(posts => console.log(posts));

        // getPosts(base_url, tag).then(posts => {
        //     posts.forEach(function (post){
        //         console.log(post)
        //     });
        //     // console.log(posts)
        // });

    });
    // console.log(test);

    res.status(200).json({ success:true })
});

// app.listen(port);
// console.log('server running at http://localhost:' + port);

app.listen(port, () => {
    console.log('server running at http://localhost:' + port);
});