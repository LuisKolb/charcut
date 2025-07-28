const candEditor = document.getElementById("candEditor");
const refEditor = document.getElementById("refEditor");
const lineCounter = document.getElementById("lineCounter");
const submitBtn = document.getElementById('submitBtn');
const compareForm = document.getElementById('compareForm');

// Function to update alternating line backgrounds based on current font metrics
function updateLineBackgrounds() {
    // Get computed styles
    const computedStyle = window.getComputedStyle(candEditor);
    const fontSize = parseFloat(computedStyle.fontSize);
    const lineHeight = parseFloat(computedStyle.lineHeight);
    
    // Calculate actual line height in pixels
    const actualLineHeight = lineHeight || (fontSize * 1.4);
    const doubleLineHeight = actualLineHeight * 2;
    
    // Create the gradient for text areas
    const textareaGradient = `repeating-linear-gradient(
        to bottom,
        transparent 0px,
        transparent ${actualLineHeight}px,
        rgba(0, 0, 0, 0.03) ${actualLineHeight}px,
        rgba(0, 0, 0, 0.03) ${doubleLineHeight}px
    )`;
    
    // Create the gradient for line counter (stronger contrast)
    const lineCounterGradient = `repeating-linear-gradient(
        to bottom,
        rgba(255, 255, 255, 0.1) 0px,
        rgba(255, 255, 255, 0.1) ${actualLineHeight}px,
        rgba(0, 0, 0, 0.1) ${actualLineHeight}px,
        rgba(0, 0, 0, 0.1) ${doubleLineHeight}px
    )`;
    
    // Apply the gradients
    candEditor.style.backgroundImage = textareaGradient;
    refEditor.style.backgroundImage = textareaGradient;
    lineCounter.style.backgroundImage = lineCounterGradient;
    
    console.log(`Updated line backgrounds: line height = ${actualLineHeight}px`);
}

// Scroll synchronization
function syncScroll(source, targets) {
    targets.forEach(target => {
        target.scrollTop = source.scrollTop;
        target.scrollLeft = source.scrollLeft;
    });
}

candEditor.addEventListener('scroll', () => {
    syncScroll(candEditor, [lineCounter, refEditor]);
});
refEditor.addEventListener('scroll', () => {
    syncScroll(refEditor, [lineCounter, candEditor]);
});

// Tab key handling
function handleTab(e, editor) {
    if (e.key === 'Tab') {
        e.preventDefault();
        const { value, selectionStart, selectionEnd } = editor;
        editor.value = value.slice(0, selectionStart) + '\t' + value.slice(selectionEnd);
        editor.setSelectionRange(selectionStart + 1, selectionStart + 1);
    }
}

candEditor.addEventListener('keydown', (e) => handleTab(e, candEditor));
refEditor.addEventListener('keydown', (e) => handleTab(e, refEditor));

// Line counter with caching
let lineCountCache = 0;
function line_counter() {
    const lineCount = Math.max(
        candEditor.value.split('\n').length,
        refEditor.value.split('\n').length
    );
    if (lineCountCache !== lineCount) {
        lineCounter.value = Array.from({ length: lineCount }, (_, i) => (i + 1) + '.').join('\n');
        lineCountCache = lineCount;
    }
}

// Submit button state management
function check_equal_lines() {
    const candLines = candEditor.value.split('\n').length;
    const refLines = refEditor.value.split('\n').length;
    const hasContent = candEditor.value.trim() !== '' || refEditor.value.trim() !== '';
    
    if (!hasContent) {
        submitBtn.disabled = true;
        submitBtn.textContent = "⚠️ No Text Provided";
    } else if (candLines === refLines) {
        submitBtn.disabled = false;
        submitBtn.textContent = "Compare Text!";
    } else {
        submitBtn.disabled = false;
        submitBtn.textContent = `⚠️ Lines: ${candLines} vs ${refLines} (will auto-fix)`;
    }
}

// Force equal line counts by padding with newlines
function forceEqualLineCounts() {
    const candLines = candEditor.value.split('\n');
    const refLines = refEditor.value.split('\n');
    const candCount = candLines.length;
    const refCount = refLines.length;
    
    if (candCount !== refCount) {
        console.log(`Fixing line count mismatch: Candidate=${candCount}, Reference=${refCount}`);
        
        if (candCount < refCount) {
            const linesToAdd = refCount - candCount;
            candEditor.value += '\n'.repeat(linesToAdd);
            console.log(`Added ${linesToAdd} lines to candidate`);
        } else {
            const linesToAdd = candCount - refCount;
            refEditor.value += '\n'.repeat(linesToAdd);
            console.log(`Added ${linesToAdd} lines to reference`);
        }
        
        line_counter();
        check_equal_lines();
        syncHeight();
        
        return true;
    }
    
    return false;
}

// Form submission safeguard
compareForm.addEventListener('submit', function(e) {
    const hasContent = candEditor.value.trim() !== '' || refEditor.value.trim() !== '';
    
    if (!hasContent) {
        e.preventDefault();
        alert('Please provide text in at least one of the text areas.');
        return false;
    }
    
    const wasFixed = forceEqualLineCounts();
    
    if (wasFixed) {
        const candCount = candEditor.value.split('\n').length;
        const refCount = refEditor.value.split('\n').length;
        console.log(`Line counts after fix: Candidate=${candCount}, Reference=${refCount}`);
        
        submitBtn.textContent = "Fixed line counts - Submitting...";
        setTimeout(() => {
            check_equal_lines();
        }, 1000);
    }
    
    const finalCandCount = candEditor.value.split('\n').length;
    const finalRefCount = refEditor.value.split('\n').length;
    
    if (finalCandCount !== finalRefCount) {
        e.preventDefault();
        alert(`Critical error: Unable to equalize line counts (${finalCandCount} vs ${finalRefCount}). Please check your text.`);
        return false;
    }
    
    return true;
});

// Debounce utility
function debounce(fn, delay) {
    let timer;
    return function(...args) {
        clearTimeout(timer);
        timer = setTimeout(() => fn.apply(this, args), delay);
    };
}

// Editor synchronization
let isSyncing = false;

function syncEditors(source, target) {
    if (isSyncing) return;
    isSyncing = true;
    const sourceLines = source.value.split('\n');
    const targetLines = target.value.split('\n');
    const diff = sourceLines.length - targetLines.length;
    if (diff > 0) {
        target.value += '\n'.repeat(diff);
    } else if (diff < 0) {
        let t = target.value.split('\n');
        while (t.length > sourceLines.length && t[t.length - 1] === '') {
            t.pop();
        }
        target.value = t.join('\n');
    }
    isSyncing = false;
}

// Debounced input handlers
const handleCandInput = debounce(() => {
    syncEditors(candEditor, refEditor);
    line_counter();
    check_equal_lines();
}, 50);

const handleRefInput = debounce(() => {
    syncEditors(refEditor, candEditor);
    line_counter();
    check_equal_lines();
}, 50);

candEditor.addEventListener('input', handleCandInput);
refEditor.addEventListener('input', handleRefInput);

// Height synchronization
function syncHeight() {
    const height = Math.max(
        candEditor.scrollHeight,
        refEditor.scrollHeight,
        window.innerHeight * 0.6
    );
    candEditor.style.height = height + 'px';
    refEditor.style.height = height + 'px';
    lineCounter.style.height = height + 'px';
}

// Use ResizeObserver for both editors
new ResizeObserver(syncHeight).observe(refEditor);
new ResizeObserver(syncHeight).observe(candEditor);

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    updateLineBackgrounds(); // Set up alternating line backgrounds
    line_counter();
    check_equal_lines();
    syncHeight();
});

// Handle paste events to maintain sync
function handlePaste(e) {
    setTimeout(() => {
        if (e.target === candEditor) {
            handleCandInput();
        } else if (e.target === refEditor) {
            handleRefInput();
        }
    }, 10);
}

candEditor.addEventListener('paste', handlePaste);
refEditor.addEventListener('paste', handlePaste);

// Update backgrounds when window is resized (in case font rendering changes)
window.addEventListener('resize', debounce(updateLineBackgrounds, 100));

// Optional: Add a toggle for line backgrounds
function addLineBackgroundToggle() {
    const toggleBtn = document.createElement('button');
    toggleBtn.type = 'button';
    toggleBtn.textContent = 'Toggle Line Stripes';
    toggleBtn.className = 'py-2 px-4 bg-gray-500 text-white rounded-md ml-2';
    
    let stripesEnabled = true;
    
    toggleBtn.onclick = () => {
        stripesEnabled = !stripesEnabled;
        if (stripesEnabled) {
            updateLineBackgrounds();
            toggleBtn.textContent = 'Hide Line Stripes';
        } else {
            candEditor.style.backgroundImage = 'none';
            refEditor.style.backgroundImage = 'none';
            lineCounter.style.backgroundImage = 'none';
            toggleBtn.textContent = 'Show Line Stripes';
        }
    };
    
    compareForm.appendChild(toggleBtn);
}

// Uncomment to add the toggle button
// addLineBackgroundToggle();