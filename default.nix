{ buildPythonPackage, fetchPypi, python311Packages, python, ... }:

buildPythonPackage {
  name = "Pfersel";
  src = ./pfersel;

  propagatedBuildInputs = with python311Packages; [

    (buildPythonPackage
      rec {
        pname = "py-cord";
        version = "2.5.0";
        propagatedBuildInputs = [
          aiohttp
          aiosignal
          attrs
          async-timeout
          charset-normalizer
          frozenlist
          idna
          multidict
          yarl
        ];

        src = fetchPypi {
          inherit pname version;
          sha256 = "sha256-+vCK9dperC7T0cikPYMH1aHj8BYC3vKDMwydLN4LEWI=";
        };
        doCheck = false;
      })
  ];

  installPhase = ''
    runHook preInstall
    mkdir -p $out/${python.sitePackages}
    cp -r . $out/${python.sitePackages}/pfersel
    runHook postInstall '';

  format = "other";
}
