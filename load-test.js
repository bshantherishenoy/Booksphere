import http from 'k6/http';

export const options = {
    vus: 1,
    iterations: 50,
};

let uniqueHosts = new Set();

export default function () {

    let res = http.get('http://13.61.152.56:31447/hostname');

    let hostname = res.body.trim();

    uniqueHosts.add(hostname);

    console.log(`Request served by: ${hostname}`);
}

export function teardown() {

    console.log("========== UNIQUE HOSTS ==========");

    console.log(JSON.stringify(Array.from(uniqueHosts), null, 2));

    console.log(`Total unique hosts: ${uniqueHosts.size}`);
}