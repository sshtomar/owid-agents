import { join } from "node:path";

process.env.OWID_DATA_DIR ??= join(process.cwd(), "data");

import { app } from "../cli/serve.js";

export default app;
