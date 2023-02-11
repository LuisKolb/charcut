let candEditor = document.getElementById("candEditor");
let refEditor = document.getElementById("refEditor");
let lineCounter = document.getElementById("lineCounter");
let submitBtn = document.getElementById('submitBtn')


candEditor.addEventListener('scroll', () => {
    lineCounter.scrollTop = candEditor.scrollTop;
    lineCounter.scrollLeft = candEditor.scrollLeft;
    refEditor.scrollTop = candEditor.scrollTop;
    refEditor.scrollLeft = candEditor.scrollLeft;
});

refEditor.addEventListener('scroll', () => {
    lineCounter.scrollTop = refEditor.scrollTop;
    lineCounter.scrollLeft = refEditor.scrollLeft;
    candEditor.scrollTop = refEditor.scrollTop;
    candEditor.scrollLeft = refEditor.scrollLeft;
});


candEditor.addEventListener('keydown', (e) => {
    let { keyCode } = e;
    let { value, selectionStart, selectionEnd } = candEditor;
if (keyCode === 9) {  // TAB = 9
      e.preventDefault();
      candEditor.value = value.slice(0, selectionStart) + '\t' + value.slice(selectionEnd);
      candEditor.setSelectionRange(selectionStart+2, selectionStart+2)
    }
});

refEditor.addEventListener('keydown', (e) => {
    let { keyCode } = e;
    let { value, selectionStart, selectionEnd } = refEditor;
if (keyCode === 9) {  // TAB = 9
      e.preventDefault();
      refEditor.value = value.slice(0, selectionStart) + '\t' + value.slice(selectionEnd);
      refEditor.setSelectionRange(selectionStart+2, selectionStart+2)
    }
});


var lineCountCache = 0;
function line_counter() {
      var lineCount = Math.max(candEditor.value.split('\n').length, refEditor.value.split('\n').length);
      var outarr = new Array();
      if (lineCountCache != lineCount) {
         for (var x = 0; x < lineCount; x++) {
            outarr[x] = (x + 1) + '.';
         }
         lineCounter.value = outarr.join('\n');
      }
      lineCountCache = lineCount;
}

function check_equal_lines() {
    if (candEditor.value == '' && refEditor.value == '') {
        submitBtn.disabled = true
        submitBtn.textContent = "⚠️ No Text Provided"
    } else if (candEditor.value.split('\n').length == refEditor.value.split('\n').length) {
        submitBtn.disabled = false
        submitBtn.textContent = "Compare Text!"
    } else {
        submitBtn.disabled = true
        submitBtn.textContent = "⚠️ Unequal Line Count"
    }
}

candEditor.addEventListener('input', () => {
    line_counter();
    let diff = candEditor.value.split('\n').length - refEditor.value.split('\n').length
    if (diff > 0) refEditor.value = refEditor.value + '\n'.repeat(diff)
    check_equal_lines()
});

refEditor.addEventListener('input', () => {
    line_counter();
    let diff = refEditor.value.split('\n').length - candEditor.value.split('\n').length
    if (diff > 0) candEditor.value = candEditor.value + '\n'.repeat(diff)
    check_equal_lines()
});



function syncHeight() {
    candEditor.offsetHeight= refEditor.offsetHeight
    lineCounter.offsetHeight = refEditor.offsetHeight
}

new ResizeObserver(syncHeight).observe(refEditor)




