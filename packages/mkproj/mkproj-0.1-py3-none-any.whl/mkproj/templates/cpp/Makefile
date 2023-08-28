CXX         ?= g++
LD          ?= g++
CXXFLAGS    = -std=c++17 -Wall -Iinclude -Wconversion -ffunction-sections -fdata-sections
LDFLAGS     = -Wl,-gc-sections
PROG_NAME   = {{ project_name }}

SRC_DIR     = src
BUILD_DIR   = build
OUT_DIR     = out
TARGET      = $(OUT_DIR)/$(PROG_NAME)
SRCS        = $(wildcard $(SRC_DIR)/*.cpp)
OBJS        = $(SRCS:$(SRC_DIR)/%.cpp=$(BUILD_DIR)/%.o)

# destination path macro we'll use below
df = $(BUILD_DIR)/$(*F)

# create a list of auto dependencies
AUTODEPS:= $(patsubst $(SRC_DIR)/%.cpp,$(BUILD_DIR)/%.d,$(SRCS))

# Rule to build the target
$(TARGET): $(OBJS) | $(OUT_DIR)
	@echo -e " [LINK]\t\t" $@
	@$(CXX) $(CXXFLAGS) $(LDFLAGS) -o $@ $^

# include by auto dependencies
-include $(AUTODEPS)

# and last but not least my generic compiler rule
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp | $(BUILD_DIR)
	@# Build the dependency file
	@$(CXX) -MM -MP -MT $(df).o -MT $(df).d $(CXXFLAGS) $< > $(df).d
	@# Compile the object file
	@echo -e " [C++]\t\t" $<
	@$(CXX) -c $< $(CXXFLAGS) -o $@

# Rule to create build directory
$(BUILD_DIR):
	@echo -e " [MKDIR]\t" $@
	@mkdir -p $(BUILD_DIR)

# Rule to create binary directory
$(OUT_DIR):
	@echo -e " [MKDIR]\t" $@
	@mkdir -p $(OUT_DIR)

# Rule to clean build artifacts
.PHONY: clean
clean:
	rm -rf $(BUILD_DIR)/* $(OUT_DIR)/*
