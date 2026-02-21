export async function run(params, context) {
    const { command } = params;
    const cmdLower = command.toLowerCase();
    
    if (cmdLower.includes("scan network") || cmdLower.includes("scent") || cmdLower.includes("sniff")) {
        context.log("Sniffing network through Pangolin-Guard...");
        try {
            const response = await fetch("http://localhost:8000/api/scent/scan");
            const data = await response.json();
            return { 
                status: "success", 
                message: `Discovered ${data.devices.length} network entities. Check the UI for details.`,
                result: data.devices 
            };
        } catch (error) {
            return { status: "error", message: "FastAPI Backend is not responding." };
        }
    }
    
    if (cmdLower.includes("panic") || cmdLower.includes("curl-up") || cmdLower.includes("arm")) {
        context.log("Activating Pangolin armor (Curl-Up Watchdog)...");
        try {
            const response = await fetch("http://localhost:8000/api/curl-up/activate", { method: "POST" });
            const data = await response.json();
            return { 
                status: "success", 
                message: "CPU Watchdog activated successfully. System is protected." 
            };
        } catch (error) {
            return { status: "error", message: "Could not activate panic protocol." };
        }
    }

    if (cmdLower.includes("search leaks") || cmdLower.includes("long tongue")) {
        context.log("Extending Long Tongue for deep leak search...");
        try {
            const response = await fetch("http://localhost:8000/api/long-tongue/search?query=secrets");
            const data = await response.json();
            return { 
                status: "success", 
                message: `Deep search completed. Found ${data.leaks.length} potential leaks.`,
                result: data.leaks
            };
        } catch (error) {
            return { status: "error", message: "Could not perform deep search." };
        }
    }

    return { 
        status: "error", 
        message: "Unknown command. Try 'scan network', 'panic', or 'search leaks'." 
    };
}