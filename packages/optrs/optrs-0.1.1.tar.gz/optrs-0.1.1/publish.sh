#!/bin/bash
maturin build --release --strip --target aarch64-apple-darwin
maturin publish
