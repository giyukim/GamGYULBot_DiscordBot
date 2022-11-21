const express = require("express");
const app = express();

let user = [
    {
        id: 1,
        name: "Hyun"
    },
    {
        id: 2,
        name: 'Alice'
    },
    {
        id: 3,
        name: 'Kelly'
    }
]

app.get('/', (req, res) => {
    res.send('Hello world!\n');
})

app.get('/users', (req, res) => {
    return res.json(users);
});

app.listen(3000, () => {
    console.log("Example app listening on port 3000");
})