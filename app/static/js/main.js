

function getFineTuneValues() {
    let vals = document.getElementsByClassName('input-values');

    res = [];
    for (let i = 0; i < vals.length; i++) {

        res.push(
            JSON.stringify(
                {
                    key: vals[i].getAttribute('id'),
                    val: vals[i].getAttribute('value')
                }
            )
        );
    }
    return res.join()
}

function getFineTune() {
    let input_tag = document.getElementById('tunes');
    input_tag.value = getFineTuneValues();
}

