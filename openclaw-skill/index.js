export async function run(params, context) {
    const { command } = params;
    const cmdLower = command.toLowerCase();
    
    if (cmdLower.includes("scaneaza retea") || cmdLower.includes("scent") || cmdLower.includes("miros")) {
        context.log("Adulmec reteaua prin Pangolin-Guard...");
        try {
            const response = await fetch("http://localhost:8000/api/scent/scan");
            const data = await response.json();
            return { 
                status: "success", 
                message: `Am descoperit ${data.devices.length} entitati in retea. Verificati UI-ul.`,
                result: data.devices 
            };
        } catch (error) {
            return { status: "error", message: "FastAPI Backend nu raspunde." };
        }
    }
    
    if (cmdLower.includes("panica") || cmdLower.includes("curl-up") || cmdLower.includes("armeaza")) {
        context.log("Activez armura Pangolin (Curl-Up Watchdog)...");
        try {
            const response = await fetch("http://localhost:8000/api/curl-up/activate", { method: "POST" });
            const data = await response.json();
            return { 
                status: "success", 
                message: "Watchdog-ul CPU a fost activat cu succes. Sistem protejat." 
            };
        } catch (error) {
            return { status: "error", message: "Nu am putut activa protocolul de panica." };
        }
    }

    return { 
        status: "error", 
        message: "Comanda necunoscuta. Incearca 'scaneaza reteaua' sau 'intra in panica'." 
    };
}