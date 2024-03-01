{ buildPythonPackage, fetchPypi, python310Packages, python, ... }:

buildPythonPackage {
  name = "Pfersel";
  src = ./pfersel;

  propagatedBuildInputs = with python310Packages; [

    (buildPythonPackage
      rec {
        pname = "py-cord";
        version = "2.4.1";
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
          sha256 = "sha256-AmbJ2anSOXYioOXq0JgmaQ5oi6PPFMRwFnuB5s0tilY=";
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
