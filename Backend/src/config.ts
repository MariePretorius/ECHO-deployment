import { config } from 'dotenv';
import * as process from "process";

config();

export const supabaseUrl = process.env.SUPABASE_URL;
export const supabaseAnonKey = process.env.SUPABASE_ANON_KEY;
export const encryptionKey = process.env.SECRET_ENCRYPTION_KEY;
export const accessKey = process.env.ACCESS_KEY;
export const youtubeKey = process.env.YOUTUBE_KEY;
export const base64Cert = process.env.SSL_CERT_BASE64;
export const base64Key = process.env.SSL_KEY_BASE64;