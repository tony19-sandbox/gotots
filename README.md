# `gotots.py`

Converts a Go struct into TypeScript class files. This is intended for structs used in JSON interfaces. The output classes are decorated with [TypedJSON](https://github.com/JohnWhiteTB/TypedJSON).

```
usage: gotots.py [-h] [-d OUTDIR] [-v] input [input ...]

Converts Go structs into TypeScript classes

positional arguments:
  input                 path to input file (Go)

optional arguments:
  -h, --help            show this help message and exit
  -d OUTDIR, --outdir OUTDIR
                        path to output directory
  -v, --verbose         print debug info while parsing
```

Example Input:

```go
package example

type StateEnum int32

const (
	StateFoo StateEnum = iota
	StateBar
	StateBaz
)

type FooStruct struct {
	FooString string `json:"my_string,omitempty"`
	FooInt int32 `json:"my_int"`
	FooState StateEnum `json:"my_state"`
}

type BarStruct struct {
	BarString string `json:"my_string"`
	BarInt int32 `json:"my_int,omitempty"`
	BarStates []StateEnum `json:"my_state"`
	BarFoo *FooStruct `json:"my_foo,omitempty"`
}
```

Example Output:

*bar-struct.ts*
```ts
import { JsonMember, JsonObject } from 'type-json'

@JsonObject
export class BarStruct {

  @JsonMember({name: 'my_string'})
  public barString: string;

  @JsonMember({name: 'my_int'})
  public barInt: number; // optional

  @JsonMember({name: 'my_state'})
  public barStates: StateEnum[];

  @JsonMember({name: 'my_foo'})
  public barFoo: FooStruct; // optional

}
```

*foo-struct.ts*
```ts
import { JsonMember, JsonObject } from 'type-json'

@JsonObject
export class FooStruct {

  @JsonMember({name: 'my_string'})
  public fooString: string; // optional

  @JsonMember({name: 'my_int'})
  public fooInt: number;

  @JsonMember({name: 'my_state'})
  public fooState: StateEnum;

}
```

*state-enum.ts*
```ts
export enum StateEnum {
  StateFoo,
  StateBar,
  StateBaz,
}
```

LICENSE
------
```
The MIT License (MIT)
Copyright (c) 2016 Anthony Trinh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
