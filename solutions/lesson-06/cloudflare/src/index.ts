import { Container, getContainer } from "@cloudflare/containers";
import { env } from "cloudflare:workers";

// One class describes the container: which port it listens on, when it may
// sleep, and which settings it receives (like `-e` in podman run).
export class HelloAi extends Container<Env> {
	defaultPort = 8000;
	sleepAfter = "10m";
	envVars = {
		MODEL_NAME: env.MODEL_NAME,
		API_KEY: env.API_KEY, // a Worker secret: npx wrangler secret put API_KEY
	};
}

// The Worker receives every request and forwards it to the container.
export default {
	async fetch(request: Request, env: Env): Promise<Response> {
		return getContainer(env.HELLO_AI).fetch(request);
	},
};
