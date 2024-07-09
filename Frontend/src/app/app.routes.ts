import { Routes } from "@angular/router";
import { LandingPageComponent } from "./pages/landing-page/landing-page.component";
import { LoginComponent } from "./pages/login/login.component";
import { RegisterComponent } from "./pages/register/register.component";
import { HomeComponent } from "./pages/home/home.component";
import { ProfileComponent } from "./pages/profile/profile.component";
import { AuthCallbackComponent } from "./authcallback/authcallback.component";
import { UserLibraryComponent } from "./pages/user-library/user-library.component";
import { ArtistProfileComponent } from "./pages/artist-profile/artist-profile.component";

export const routes: Routes = [
  { path: "landing", component: LandingPageComponent },
  { path: "login", component: LoginComponent },
  { path: "register", component: RegisterComponent },
  { path: "home", component: HomeComponent },
  { path: "profile", component: ProfileComponent },
  { path: "auth/callback", component: AuthCallbackComponent },
  { path: "", redirectTo: "/login", pathMatch: "full" },
  { path: "library", component: UserLibraryComponent},
  { path: "artist-profile", component: ArtistProfileComponent}
  //{ path: "**", redirectTo: "/login", pathMatch: "full" },
];
