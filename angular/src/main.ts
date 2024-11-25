import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';

//rJyCTPO03OikwN4xc9ViIaAJWX7H/d5PTsAZAZJ0N9Om3TIBgO8ijXlrhmodc0MhKtZVPE/MZv8fz0UYVIaBkwTjpDxu8XMHXb/pYta6R+plb1JzV55vYf3RhfWuC375Zd0VUqlg6N+9vInMX+2ym0zQ7ZDim8pzSAqEP+MzNYfLMAnU86Za0DPadTecvKZU
bootstrapApplication(AppComponent, appConfig)
  .catch((err) => console.error(err));
