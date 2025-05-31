
async function askAI() {
    const prompt = document.getElementById("prompt").value

    const res = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
            prompt: prompt
        })
    })

    const data = await res.json()
    
    document.getElementById("response").innerHTML = data.response
    console.log("cached response:", data.cached)
}