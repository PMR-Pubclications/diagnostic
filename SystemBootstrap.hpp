#include <iostream>
#include <filesystem>
#include <system_error>

namespace fs = std::filesystem;

class SystemBootstrap {
public:
    struct SystemPaths {
        fs::path trustMainRoot;
        fs::path trustShellRoot;
        fs::path avEngineRoot;
    };

    static bool InitializeAndVerifySystem(const SystemPaths& paths) {
        std::cout << "[Bootstrap] Starting independent system diagnostics & initialization...\n";
        bool systemHealthy = true;

        // 1. Audit Trust-Main Security Assets
        fs::path mainKey = paths.trustMainRoot / "certs" / "client.key";
        fs::path mainCsr = paths.trustMainRoot / "certs" / "client.csr";
        if (fs::exists(mainKey) && fs::exists(mainCsr)) {
            std::cout << "  [PASS] Trust-Main cryptographic assets verified.\n";
        } else {
            std::cerr << "  [FAIL] Trust-Main missing keys or CSRs in: " << paths.trustMainRoot << "\n";
            systemHealthy = false;
        }

        // 2. Audit Trust-Shell Integration
        fs::path shellCert = paths.trustShellRoot / "client.crt";
        if (fs::exists(shellCert)) {
            std::cout << "  [PASS] Trust-Shell client certificate linked successfully.\n";
        } else {
            std::cerr << "  [FAIL] Trust-Shell client certificate missing at: " << shellCert << "\n";
            systemHealthy = false;
        }

        // 3. Audit AudioVideoEngine-CPP Assets
        fs::path engineCa = paths.avEngineRoot / "localCA.crt";
        if (fs::exists(engineCa)) {
            std::cout << "  [PASS] AudioVideoEngine-CPP Root CA (localCA.crt) verified.\n";
        } else {
            std::cerr << "  [FAIL] AudioVideoEngine-CPP missing localCA.crt at: " << engineCa << "\n";
            systemHealthy = false;
        }

        if (systemHealthy) {
            std::cout << "[Bootstrap] All subsystems verified. System ready for secure mTLS handshake.\n";
        } else {
            std::cerr << "[Bootstrap] CRITICAL: System verification failed. Aborting startup sequence.\n";
        }

        return systemHealthy;
    }
};
