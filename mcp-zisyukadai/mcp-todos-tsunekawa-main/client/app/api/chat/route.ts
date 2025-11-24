import { google } from "@ai-sdk/google";
import { streamText, experimental_createMCPClient as createMcpClient } from "ai";

export async function POST(request: Request) {
  let mcpClient: any = null;
  try {
    console.log("[API] Chat request received");

    try {
      console.log("[API] Creating MCP client...");
      mcpClient = await createMcpClient({
        transport: {
          type: "sse",
          url: "http://localhost:3001/sse",
        },
      });
      console.log("[API] MCP client created successfully");
    } catch (err) {
      console.error("[API] Failed to create MCP client:", err);
      throw new Error(`MCP Client Error: ${err instanceof Error ? err.message : String(err)}`);
    }

    const { messages } = await request.json();
    console.log("[API] Messages received:", messages.length);

    let tools;
    try {
      console.log("[API] Fetching tools from MCP server...");
      tools = await mcpClient.tools();
      console.log("[API] Tools retrieved:", Object.keys(tools || {}).length);
    } catch (err) {
      console.error("[API] Failed to fetch tools:", err);
      throw new Error(`Tools Error: ${err instanceof Error ? err.message : String(err)}`);
    }

    console.log("[API] Calling streamText...");
    const result = streamText({
      model: google("gemini-2.0-flash-lite"),
      messages,
      tools,
      onFinish: () => {
        console.log("[API] Stream finished, closing MCP client");
        mcpClient?.close();
      },
    });

    console.log("[API] Returning data stream response");
    return result.toDataStreamResponse();
  } catch (error) {
    console.error("[API] Error in POST handler:", error);
    if (mcpClient) {
      try {
        mcpClient.close();
      } catch (e) {
        console.error("[API] Error closing MCP client:", e);
      }
    }
    return new Response(
      JSON.stringify({
        error: error instanceof Error ? error.message : String(error),
      }),
      { status: 500, headers: { "Content-Type": "application/json" } }
    );
  }
}
