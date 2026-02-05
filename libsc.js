const HOST = "77.239.125.65";
const PORT = "9338";
const STAGE_ADDRESS = 0x96C2F4;
const ADD_FILE = 0x24F5C0;

var malloc = new NativeFunction(Module.findExportByName('libc.so', 'malloc'), 'pointer', ['int']);

const hook = Interceptor.attach;

function createStringPtr(message) {
    var charPtr = malloc(message.length + 1);
    Memory.writeUtf8String(charPtr, message);
    return charPtr
}

const Libg = {
	init() {
		this.base = Module.findBaseAddress('libg.so');
		
		this.NativeFont = {
			addr: {}
		};
		
		this.NativeFont.addr.formatString = this.offset(0x44C26C);
		this.isLicenseCheckRequired = this.offset(0x3F5598);
		this.HomePageStartGame = this.offset(0x3ED6DC);
	},
	offset(off) {
		return this.base.add(off);
	}
}

const CLIENT_SECRET_KEY = [0xBB, 0x14, 0xD6, 0xFD, 0x2B, 0x7C, 0x98, 0x23, 0xEA, 0xED, 0xB4, 0x33, 0x8C, 0xB7, 0x23, 0x7F, 0x61, 0xE4, 0x22, 0xD2, 0x3C, 0x49, 0x77, 0xF7, 0x4A, 0xDA, 0x05, 0x27, 0x02, 0xC0, 0xC6, 0x2D];
const EncryptionPatcher = {
	init() {
		Interceptor.attach(Libg.offset(0x158358), {
            onEnter(args) {
                this.buffer = args[0];
            },
            onLeave(retval) {
                this.buffer.writeByteArray(CLIENT_SECRET_KEY);
            }
        });
	}
}

const AddFiler = {
	init(scfile) {
		const AddFile = new NativeFunction(Libg.offset(ADD_FILE), 'int', ['pointer', 'pointer', 'int', 'int', 'int', 'int']);
		hook(Libg.offset(0x24F5C0), {
			onEnter(args) {
				AddFile(args[0], createStringPtr(scfile), -1, -1, -1, -1);
			}
		});
	}
}

const Redirection = {
	init(targetHost, targetPort) {
		hook(Module.findExportByName('libc.so', 'getaddrinfo'), {
			onEnter(args) {
				this.str = args[0] = Memory.allocUtf8String(targetHost);
				args[1].writeUtf8String(targetPort);
			}
		});
	}
}

const GamePatcher = {
	init() {
		GamePatcher.enableColorCodes();
		GamePatcher.enableHomePageStartGame();
	},
	enableColorCodes() {
		hook(Libg.NativeFont.addr.formatString, {
			onEnter(args) {
				args[7] = ptr(1);
			}
		});
	},
	enableHomePageStartGame() {
		hook(Libg.HomePageStartGame, {
			onEnter(args) {
				args[3] = ptr(3);
			}
		});
	}
}

const ArxanPatcher = {
	init() {
		RuntimePatcher.jmp(Libg.offset(0x5B708), Libg.offset(0x5C664));
		RuntimePatcher.jmp(Libg.offset(0x30DD58), Libg.offset(0x30EBBC));
		RuntimePatcher.jmp(Libg.offset(0x7B78C), Libg.offset(0x7C9C0));
		RuntimePatcher.jmp(Libg.offset(0x4723C0), Libg.offset(0x4735C0));
		
		hook(Libg.offset(0x4E1494), function() {
			this.context.r1 = 228;
			this.context.r2 = 228;
		})
	}
}

rpc.exports.init = function() {
	Libg.init();
	ArxanPatcher.init();
	Redirection.init(HOST, PORT);
	EncryptionPatcher.init();
	GamePatcher.init();
	AddFiler.init("sc/debug.sc");
}

const RuntimePatcher = {
	nop: function(addr) {
		Memory.patchCode(addr, Process.pageSize, function(code) {
			var writer = new ArmWriter(code, {
				pc: addr
			});
			
			writer.putNop();
			writer.flush();
		});
	},
    ret: function(addr) {
		Memory.patchCode(addr, Process.pageSize, function(code) {
			var writer = new ArmWriter(code, {
				pc: addr
			});
			
			writer.putRet();
			writer.flush();
		});
	},
	jmp: function(addr, target) {
		Memory.patchCode(addr, Process.pageSize, function(code) {
			var writer = new ArmWriter(code, {
				pc: addr
			});
			
			writer.putBranchAddress(target);
			writer.flush();
		});
	}
}