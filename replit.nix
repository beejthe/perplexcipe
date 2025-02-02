{ pkgs }: {
  deps = [
    pkgs.python310
    pkgs.python310Packages.flask
    pkgs.python310Packages.flask-cors
    pkgs.python310Packages.python-dotenv
    pkgs.python310Packages.httpx
    pkgs.nodePackages.vercel
  ];
} 