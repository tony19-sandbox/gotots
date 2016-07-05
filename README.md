# `gotots.py`

Converts a Go struct into TypeScript class files. This is intended for structs used in JSON interfaces. The output classes are decorated with TypedJSON.

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
