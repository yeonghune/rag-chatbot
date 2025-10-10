export interface SignInRequest {
  username: string;
  password: string;
}

export interface User {
  userId: number;
  name: string;
  userRole: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export type SignInResponse = TokenResponse;
