#include <iostream>
#include "SystemDiagnostics.hpp"

int main() {
    std::cout << "[*] Initializing Diagnostic Core Audit Suite...\n";

    bool auditPassed = SystemDiagnostics::RunFullDiagnosticAudit();

    if (auditPassed) {
        std::cout << "[+] Diagnostic audit successfully completed. All systems nominal.\n";
        return 0;
    } else {
        std::cerr << "[-] Diagnostic audit failed. Review transparency logs above for details.\n";
        return 1;
    }
}
