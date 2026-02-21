/**
 * No external dependencies (like axios or specific libraries) are required.
 * OpenClaw runtime provides `fetch` globally (native Node.js >= 18).
 * The context object provides logging capabilities.
 */
export async function run(params, context) {
    const { command } = params;
    const cmdLower = command.toLowerCase();
    
    // Scent Module: Network Discovery
    if (cmdLower.includes("scan network") || cmdLower.includes("scent") || cmdLower.includes("sniff")) {
        context.log("Sniffing network through Pangolin-Guard...");
        try {
            const response = await fetch("http://localhost:8000/api/scent/scan");
            if (!response.ok) throw new Error("API returned an error");
            const data = await response.json();
            return { 
                status: "success", 
                message: `Discovered ${data.devices.length} network entities. They have been logged in the local SQLite database.`,
                result: data.devices 
            };
        } catch (error) {
            return { status: "error", message: "FastAPI Backend is not responding. Ensure it is running on port 8000." };
        }
    }
    
    // Curl-Up Module: CPU Watchdog Panic Mode
    if (cmdLower.includes("panic") || cmdLower.includes("curl-up") || cmdLower.includes("arm")) {
        context.log("Activating Pangolin armor (Curl-Up Watchdog)...");
        try {
            const response = await fetch("http://localhost:8000/api/curl-up/activate", { method: "POST" });
            if (!response.ok) throw new Error("API returned an error");
            return { 
                status: "success", 
                message: "CPU Watchdog activated successfully. System is protected and monitoring for CPU spikes." 
            };
        } catch (error) {
            return { status: "error", message: "Could not activate panic protocol. Ensure FastAPI Backend is running." };
        }
    }

    // Long Tongue Module: Deep Leak Search
    if (cmdLower.includes("search leaks") || cmdLower.includes("long tongue")) {
        context.log("Extending Long Tongue for deep leak search...");
        try {
            const response = await fetch("http://localhost:8000/api/long-tongue/search?query=secrets");
            if (!response.ok) throw new Error("API returned an error");
            const data = await response.json();
            return { 
                status: "success", 
                message: `Deep search completed. Found ${data.leaks.length} potential leaks. Logged to database.`,
                result: data.leaks
            };
        } catch (error) {
            return { status: "error", message: "Could not perform deep search. Ensure FastAPI Backend is running." };
        }
    }

    return { 
        status: "error", 
        message: "Unknown command. Try 'scan network', 'panic', or 'search leaks'." 
    };
}